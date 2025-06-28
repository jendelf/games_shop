from typing import Annotated, Any
import jwt
from settings import settings
from .schemas import UserInDB, TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from .models import User
from .service import verify_password

#TODO УБРАТЬ СЛОВАРЬ ПОТОМ ЗАМЕНИТЬ НА РЕАЛЬНУЮ БД
fake_users_db = {
    "johndoe@example.com": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$examplehashedpassword",
        "disabled": False,
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(user_db, email: str): # retrieves a user from DB by email
    if email in user_db:
        user_dict = user_db[email]
        return UserInDB(**user_dict)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict[str, Any] = jwt.decode(token, key = settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email = email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, email=token_data.email) #TODO ЗАМЕНИТЬ fake_users_db на настоящую БД
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)], 
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def authenticate_user(fake_users_db, email: str, password: str): #TODO ЗАМЕНИТЬ fake_users_db на настоящую БД
    user = get_user(fake_users_db, email) 
    if not user:
        return False
    if not verify_password(password, user.hashed_password): 
        return False
    return user 