from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from .schemas import UserOut, UserIn, TokenPair
from .dependencies import get_current_active_user, get_session, require_role
from .user_repository import (
    login_for_access_token, get_users_games,
    user_registration, refresh_access_token, user_logout
)
from .admin_repository import get_all_users, ban_user, update_user_role
from .models import User
from src.shop.schemas import GameOut
from src.role import Role
from .exceptions import RefreshTokenMissing

router = APIRouter()
#AUTH API
# -----------------------------------------------------------------------------------------------

@router.post("/register")
async def register(user: UserIn, session: AsyncSession = Depends(get_session)):
    print("Received user:", user.dict())
    new_user = await user_registration(user, session)
    return new_user

@router.post("/token", response_model=TokenPair)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    return await login_for_access_token(form_data, session)

@router.post("/refresh", response_model=TokenPair)
async def refresh(request: Request, session: AsyncSession = Depends(get_session)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise RefreshTokenMissing
    return await refresh_access_token(refresh_token, session)

@router.post("/logout")
async def logout(request: Request, session: AsyncSession = Depends(get_session)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await user_logout(refresh_token, session)
    return {"detail": "Logged out"}

# USER API
# ---------------------------------------------------------------------------------

@router.get("/me", response_model=UserOut)
async def get_current_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@router.get("/me/library", response_model=list[GameOut])
async def get_library(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session)
):
    return await get_users_games(current_user, session)

#ADMIN API
# -----------------------------------------------------------------------------------

@router.get("/admin/users", response_model=list[UserOut])
async def admin_get_users(
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_role(Role.ADMIN))
):
    return await get_all_users(session)

@router.post("/admin/ban")
async def admin_ban_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_role(Role.ADMIN))
):
    await ban_user(user_id, session)
    return {"detail": f"User {user_id} banned"}

@router.post("/admin/set-role")
async def admin_set_role(
    user_id: int,
    role: Role,  
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_role(Role.ADMIN))
):
    await update_user_role(user_id, role, session)
    return {"detail": f"Role updated to {role}"}