from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserOut, UserIn
from .dependencies import active_user_dep, DB_session_dep, require_role
from .user_repository import (
    login_for_access_token, get_users_games,
    user_registration, refresh_access_token, user_logout
)
from .admin_repository import get_all_users, ban_user, update_user_role
from .models import User
from src.shop.schemas import GameOut
from src.role import Role
from .utils import get_user

router = APIRouter()
templates = Jinja2Templates(directory="src/auth/static/templates")

# ---------------- HTML pages ----------------

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "action": "/auth/token", 
        "switch_text": "Don't have an account?",
        "switch_url": "/auth/register",
        "switch_action": "Register"
    })


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/panel", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    session: AsyncSession = DB_session_dep,
    user: User = Depends(require_role(Role.ADMIN))
):
    users = await get_all_users(session)
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "users": users})


# ---------------- Form submissions ----------------

@router.post("/token")
async def login_form(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = DB_session_dep
):
    form_data = OAuth2PasswordRequestForm(username=username, password=password, scope="")
    tokens = await login_for_access_token(form_data, session)
    user = await get_user(session, form_data.username)

    # Определяем, куда редиректить: в админку или в магазин
    redirect_url = "/auth/panel" if user.role == Role.ADMIN else "/shop"
    
    # Возвращаем RedirectResponse с куками
    response = RedirectResponse(url=redirect_url, status_code=303)
    response.set_cookie("access_token", tokens.access_token, httponly=True)
    response.set_cookie("refresh_token", tokens.refresh_token, httponly=True)
    return response

@router.post("/register")
async def register_form(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = DB_session_dep
):
    user = UserIn(username=username, email=email, password=password)
    await user_registration(user, session)
    return RedirectResponse(url="/auth/login", status_code=302)


@router.post("/logout")
async def logout_view(
    request: Request,
    session: AsyncSession = DB_session_dep
):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await user_logout(refresh_token, session)

    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@router.post("/panel/ban")
async def ban_user_view(
    user_id: int = Form(...),
    session: AsyncSession = DB_session_dep,
    _: User = Depends(require_role(Role.ADMIN))
):
    await ban_user(user_id, session)
    return RedirectResponse(url="/auth/panel", status_code=303)


@router.post("/panel/set-role")
async def set_role_view(
    user_id: int = Form(...),
    role: str = Form(...),  # Firstly get a string
    session: AsyncSession = DB_session_dep,
    _: User = Depends(require_role(Role.ADMIN))
):
    try:
        role_enum = Role(role)  # Then make enum
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role")

    await update_user_role(user_id, role_enum, session)
    return RedirectResponse(url="/auth/panel", status_code=303)


# ---------------- API endpoints ----------------

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: Annotated[UserOut, active_user_dep]):
    return current_user


@router.get("/me/library", response_model=list[GameOut])
async def get_user_library(
    current_user: Annotated[UserOut, active_user_dep],
    session: AsyncSession = DB_session_dep
):
    return await get_users_games(current_user, session)
