from fastapi import APIRouter, Depends, status, HTTPException
from .schemas import PageParams, GameCreate, IdSchema, GameUpdate, PaginatedResponse, GameOut
from .dependencies import get_pagination_params
from .service.game import (
    get_paginated_games, create_game_service, delete_game_service, 
    update_game_service, get_game_info_service,
)
from src.database import async_session_maker, get_session
from src.auth.dependencies import get_current_user
from src.auth.schemas import UserOut
from .exceptions import GameNotFound, GameAlreadyExist, PermissionDenied

router = APIRouter(tags=["shop"])

@router.get("/", response_model=PaginatedResponse)
async def shop_page(
    pagination: PageParams = Depends(get_pagination_params),
    session = Depends(get_session)
):
    return await get_paginated_games(session, pagination)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_game_post(
    game_data: GameCreate,
    current_user: UserOut = Depends(get_current_user),
    session = Depends(get_session)
):
    try:
        await create_game_service(session, game_data, owner_id=current_user.id)
        return {"message": "Game created successfully"}
    except GameAlreadyExist as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/delete")
async def delete_game_post(
    payload: IdSchema,
    current_user: UserOut = Depends(get_current_user),
    session = Depends(get_session)
):
    try:
        await delete_game_service(session, payload.id, user_id=current_user.id)
        return {"id": payload.id, "message": "Game deleted successfully!"}
    except GameNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionDenied as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/update")
async def update_game_post(
    game_data: GameUpdate,
    current_user: UserOut = Depends(get_current_user),
    session = Depends(get_session)
):
    try:
        await update_game_service(session, game_data.id, game_data, user_id=current_user.id)
        return {"id": game_data.id, "message": "Game updated successfully"}
    except GameNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionDenied as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/game_info")
async def get_game_info(
    payload: IdSchema,
    session = Depends(get_session)
):
    try:
        return await get_game_info_service(session, payload.id)
    except GameNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/wishlist")
async def add_wishlist_post(
    payload: IdSchema,
    current_user: UserOut = Depends(get_current_user),
    session = Depends(get_session)
):
    await add_wishlist_service(session, payload.id, user_id=current_user.id)
    return {"id": payload.id, "message": "Game added to wishlist!"}


@router.post("/buy")
async def buy_game_post(
    payload: IdSchema,
    current_user: UserOut = Depends(get_current_user),
    session = Depends(get_session)
):
    await buy_game_service(session, payload.id, user_id=current_user.id)
    return {"id": payload.id, "message": "Game purchased successfully!"}


@router.post("/cart")
async def add_cart_post(
    payload: IdSchema,
    current_user: UserOut = Depends(get_current_user),
    session = Depends(get_session)
):
    cart = await add_cart_service(session, payload.id, user_id=current_user.id)
    return cart
