from fastapi import APIRouter, Depends, Request,  Form, status
from fastapi.templating import Jinja2Templates
from .schemas import PageParams, GameCreate
from .dependencies import get_pagination_params
from .service.game import get_paginated_games, create_game_service
from src.database import async_session_maker
from fastapi.responses import RedirectResponse
from src.auth.dependencies import get_current_user
from src.auth.schemas import UserOut

import json
router = APIRouter()
templates = Jinja2Templates(directory="src/shop/static/templates")

@router.get("/")
async def shop_page(
    request: Request,
    pagination: PageParams = Depends(get_pagination_params)
):
    async with async_session_maker() as session:
        result = await get_paginated_games(session, pagination)
        return templates.TemplateResponse("shop.html", {
            "request": request,
            **result
        })

@router.get("/add")
async def add_game_form(request: Request):
    return templates.TemplateResponse("game_add.html", {"request": request})

@router.post("/add")
async def add_game_post(
    request: Request,
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    genres: str = Form(...),
    photos_url: str = Form(...),
    current_user: UserOut = Depends(get_current_user),  
):
    game_data = GameCreate(
        name=name,
        description=description,
        price=price,
        genres=json.loads(genres),
        photos_url=json.loads(photos_url),
    )

    await create_game_service(game_data, owner_id=current_user.id)
    return RedirectResponse(url="/shop/", status_code=status.HTTP_303_SEE_OTHER)
