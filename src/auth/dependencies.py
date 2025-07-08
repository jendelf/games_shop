from typing import Annotated, Any
import jwt
from src.settings import settings
from .schemas import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from .models import User
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .service import get_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: AsyncSession = Depends(get_session)):

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
    user = await get_user(session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)], 
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

DB_session_dep = Depends(get_session)
current_user_dep = Depends(get_current_user)
active_user_dep = Depends(get_current_active_user)