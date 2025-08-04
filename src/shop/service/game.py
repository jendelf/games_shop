from sqlalchemy.ext.asyncio import AsyncSession
from src.shop.game_repository import GameRepository
from src.shop.schemas import PageParams, GameCreate, GameOut, GameUpdate

async def get_paginated_games(session: AsyncSession, pagination: PageParams):
    total = await GameRepository.count_items(session)
    items = await GameRepository.get_items_with_pagination(session, pagination)
    
    total_pages = (total + pagination.page_size - 1) // pagination.page_size

    return {
        "items": items,
        "total": total,
        "total_pages": total_pages,
        "page": pagination.page,
        "page_size": pagination.page_size,
    }

async def create_game_service(game_data: GameCreate, owner_id: int):
    full_data = game_data.model_dump()
    full_data["owner_id"] = owner_id
    return await GameRepository.add_game(game_data.name, GameCreate(**full_data))

async def update_game_service(game_id: int, data: GameUpdate):
    return await GameRepository.update_game(game_id, data)

async def delete_game_service(game_id: int):
    return await GameRepository.delete_game(game_id)