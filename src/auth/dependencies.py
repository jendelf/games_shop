from typing import Annotated, Any

from fastapi import Depends, HTTPException, status, Request
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import decode, exceptions as jwt_exceptions

from src.settings import settings
from .schemas import TokenData
from .models import User
from .user_repository import get_user
from src.database import get_session
from src.role import Role


async def get_token_from_request(request: Request) -> str:
    
    auth_header = request.headers.get("Authorization")
    if auth_header:
        scheme, token = get_authorization_scheme_param(auth_header)
        if scheme and scheme.lower() == "bearer" and token:
            return token

    token = request.cookies.get("access_token")
    if token:
        return token

    # If nothing found
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> User:
    token = await get_token_from_request(request)

    try:
        payload: dict[str, Any] = decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception()
        token_data = TokenData(email=email)
    except jwt_exceptions.InvalidTokenError:
        raise credentials_exception()

    user = await get_user(session, email=token_data.email)
    if user is None:
        raise credentials_exception()

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(required_role: Role):
    def wrapper(user: User = Depends(get_current_active_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return wrapper


DB_session_dep = Depends(get_session)
current_user_dep = Depends(get_current_user)
active_user_dep = Depends(get_current_active_user)


def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
