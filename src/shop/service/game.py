from sqlalchemy.ext.asyncio import AsyncSession
from src.shop.game_repository import GameRepository
from src.shop.schemas import PageParams, GameCreate, GameOut, GameUpdate
from typing import List, Dict, Any
from src.shop.models import Game
from sqlalchemy import select, desc, func

async def get_paginated_games(session: AsyncSession, pagination: PageParams) -> Dict[str, Any]:

    query = await session.execute(
        select(Game)
        .order_by(Game.positive_ratings.desc())
        .limit(pagination.limit)
        .offset(pagination.offset)
    )
    games: List[Game] = query.scalars().all()
    
    total_count_query = await session.execute(select(func.count(Game.appid)))
    total_count = total_count_query.scalar()
    
    return {
        "games": [
            GameOut.model_validate({
                **game.__dict__,
                "image_url": game.image_url
            }) for game in games
        ],
        "total": total_count,
        "page": pagination.page,
        "page_size": pagination.page_size,
        "total_pages": (total_count + pagination.page_size - 1) // pagination.page_size
    }

from src.shop.models import Game
from src.shop.schemas import GameCreate, GameUpdate, GameOut, PageParams
from src.shop.exceptions import GameNotFound, GameAlreadyExist, PermissionDenied
from src.shop.game_repository import GameRepository
from src.database import async_session_maker


async def create_game_service(game_data: GameCreate, owner_id: int) -> GameOut:
    async with async_session_maker() as session:
        existing = await GameRepository.get_by_title(session, game_data.name)
        if existing:
            raise GameAlreadyExist(game_data.name)

        game = Game(**game_data.model_dump(), owner_id=owner_id)
        game = await GameRepository.add(session, game)
        return GameOut.model_validate(game)


async def update_game_service(game_id: int, data: GameUpdate, user_id: int) -> GameOut:
    async with async_session_maker() as session:
        game = await GameRepository.get_by_id(session, game_id)
        if not game:
            raise GameNotFound(game_id)

        if game.owner_id != user_id:
            raise PermissionDenied("You cannot update this game")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(game, key, value)

        updated = await GameRepository.update(session, game)
        return GameOut.model_validate(updated)


async def delete_game_service(game_id: int, user_id: int) -> dict:
    async with async_session_maker() as session:
        game = await GameRepository.get_by_id(session, game_id)
        if not game:
            raise GameNotFound(game_id)

        if game.owner_id != user_id:
            raise PermissionDenied("You cannot delete this game")

        await GameRepository.delete(session, game)
        return {"id": game_id, "message": f"Game '{game.name}' deleted successfully"}
