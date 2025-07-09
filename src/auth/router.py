from typing import Annotated
from .schemas import UserOut
from fastapi import APIRouter, Depends
from .dependencies import active_user_dep, DB_session_dep
from sqlalchemy.ext.asyncio import AsyncSession
from .service import login_for_access_token, get_users_games, user_registration, refresh_access_token, user_logout
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import Token, UserIn, TokenPair
from src.shop.schemas import GameOut


router = APIRouter()
@router.post("/registration", response_model=UserOut)
async def registration(form_data: Annotated[UserIn, Depends()],
                       session: AsyncSession = DB_session_dep):
    return await user_registration(form_data, session)

@router.post("/token", response_model=TokenPair)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = DB_session_dep,
):
    return await login_for_access_token(form_data, session)

@router.get("/users/me/", response_model=UserOut)
async def read_users_me(
    current_user: Annotated[UserOut, active_user_dep],
):
    return current_user


@router.get("/users/me/library/", response_model=list[GameOut])
async def get_user_library(current_user: Annotated[UserOut, active_user_dep],
                           session: AsyncSession = DB_session_dep
                           ):
    return await get_users_games(current_user, session)

@router.post("/refresh", response_model=Token)
async def refresh(refresh_token: str, session: AsyncSession = DB_session_dep):
    return await refresh_access_token(refresh_token, session)

@router.post("/logout")
async def logout(refresh_token: str, session: AsyncSession = DB_session_dep):
    return await user_logout(refresh_token, session)
