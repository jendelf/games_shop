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

async def create_game_service(game_data: GameCreate, owner_id: int) -> GameOut:
    full_data = game_data.model_copy(update={"owner_id": owner_id})
    game = await GameRepository.add_game(full_data)
    return GameOut.model_validate(game)

async def update_game_service(game_id: int, data: GameUpdate) -> GameOut:
    updated_game = await GameRepository.update_game(game_id, data)
    return GameOut.model_validate(updated_game)

async def delete_game_service(game_id: int) -> dict:
    await GameRepository.delete_game(game_id)
    return {"id": game_id, "message": "Game deleted successfully"}