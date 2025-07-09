from datetime import datetime, timedelta, timezone
import jwt
from src.settings import settings
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserIn, TokenPair
from .constants import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from src.shop.models import Game
from .models import User, RefreshToken
from .dependencies import DB_session_dep
from .exceptions import (
    InvalidCredentials,
    RefreshTokenExpired,
    InvalidRefreshToken,
    RefreshTokenNotFound,
    UserAlreadyExists
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user(session: AsyncSession, email: str): # retrieves a user from DB by email
    query = select(User).where (User.email==email) 
    result = await session.execute(query)
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
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

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
        raise UserAlreadyExists
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

async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm,
    session: AsyncSession
) -> TokenPair:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise InvalidCredentials

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    db_token = RefreshToken(token=refresh_token, user_id=user.id)
    session.add(db_token)
    await session.commit()

    return TokenPair(access_token=access_token, refresh_token=refresh_token)

async def user_logout(refresh_token: str, session: AsyncSession = DB_session_dep):
    stmt = select(RefreshToken).where(RefreshToken.token == refresh_token)
    result = await session.execute(stmt)
    token_obj = result.scalar_one_or_none()
    if token_obj:
        await session.delete(token_obj)
        await session.commit()
    return {"detail": "Logged out"}

async def refresh_access_token(refresh_token: str, session: AsyncSession = DB_session_dep):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise RefreshTokenExpired
    except jwt.InvalidTokenError:
        raise InvalidRefreshToken

    stmt = select(RefreshToken).where(RefreshToken.token == refresh_token)
    result = await session.execute(stmt)
    token_obj = result.scalar_one_or_none()

    if not token_obj:
        raise RefreshTokenNotFound

    new_access_token = create_access_token({"sub": email})
    return {"access_token": new_access_token, "token_type": "bearer"}