from datetime import datetime, timedelta, timezone
import jwt
from src.settings import settings
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import Token, UserIn
from .constants import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from src.shop.models import Game
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user(session: AsyncSession, email: str): # retrieves a user from DB by email
    select_user = select(User).where (User.email==email) 
    result = await session.execute(select_user)
    user = result.scalar_one_or_none()
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm,
    session: AsyncSession
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

async def get_users_games(user: User, session: AsyncSession):
    query = select(Game).where(Game.owner_id == user.id)
    result = await session.execute(query)
    return result.scalars().all()

async def authenticate_user(email: str, password: str, session: AsyncSession): 
    user = await get_user(session, email) 
    if not user:
        return False
    if not verify_password(password, user.hashed_password): 
        return False
    return user 

async def user_registration(user_data: UserIn, session: AsyncSession) -> User:
    query = select(User).where(User.email == user_data.email)
    result = await session.execute(query)
    if result.scalar_one_or_none():
        raise ValueError(f"User with '{user_data.email}' already exists")
    hashed_password = get_password_hash(user_data.password)
    new_user = User(username = user_data.username,
                    hashed_password = hashed_password,
                    email = user_data.email,
                    disabled = user_data.disabled,
                    balance = user_data.balance
                    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
#TODO написать функцию log out
async def logout():
    pass