from fastapi import APIRouter, Depends, status
from .schemas import PageParams, GameCreate, IdSchema, GameUpdate, PaginatedResponse, GameOut
from .dependencies import get_pagination_params
from .service.game import get_paginated_games, create_game_service, delete_game_service, update_game_service
from src.database import async_session_maker
from src.auth.dependencies import get_current_user
from src.auth.schemas import UserOut
from typing import List
from .models import Game
from .exceptions import GameNotFound

router = APIRouter(tags=["shop"])

@router.get("/", response_model=PaginatedResponse)
async def shop_page(pagination: PageParams = Depends(get_pagination_params)):
    async with async_session_maker() as session:
        return await get_paginated_games(session, pagination)

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_game_post(
    game_data: GameCreate,
    current_user: UserOut = Depends(get_current_user),
):
    await create_game_service(game_data, owner_id=current_user.id)
    return {"message": "Game created successfully"}

@router.post("/delete")
async def delete_game_post(payload: IdSchema):
    game_id = payload.id
    await delete_game_service(game_id)
    return {"id": game_id, "message": "Game deleted successfully!"}

@router.post("/update")
async def update_game_post(game_data: GameUpdate):
    await update_game_service(game_data)
    return {"id": game_data, "message": "Game updated successfully"}

@router.post("/game_info")
async def get_game_info(payload: IdSchema):
    async with async_session_maker() as session:
        game = await session.get(Game, payload.id)
        if not game:
            raise GameNotFound
        return GameOut.model_validate(game)

@router.post("/wishlist", response_model=dict)
async def add_wishlist_post(payload: IdSchema, current_user: UserOut = Depends(get_current_user)):
    game_id = payload.id
    await add_wishlist_service(game_id, user_id=current_user.id)
    return {"id": game_id, "message": "Game added to wishlist!"}