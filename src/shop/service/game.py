from typing import List, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.shop.models import Game
from src.shop.exceptions import GameNotFound, GameAlreadyExist, PermissionDenied
from src.shop.game_repository import GameRepository
from src.shop.schemas import PageParams, GameCreate, GameOut, GameUpdate


async def get_paginated_games(session: AsyncSession, pagination: PageParams) -> Dict[str, Any]:
    games: List[Game] = await GameRepository.get_paginated(session, pagination.limit, pagination.offset)
    total_count: int = await GameRepository.count_all(session)

    return {
        "games": [GameOut.model_validate(game) for game in games],
        "total": total_count,
        "page": pagination.page,
        "page_size": pagination.page_size,
        "total_pages": (total_count + pagination.page_size - 1) // pagination.page_size
    }


async def create_game_service(session: AsyncSession, game_data: GameCreate, owner_id: int) -> GameOut:
    existing = await GameRepository.get_by_title(session, game_data.name)
    if existing:
        raise GameAlreadyExist(game_data.name)

    game = Game(**game_data.model_dump(), owner_id=owner_id)
    game = await GameRepository.add(session, game)
    return GameOut.model_validate(game)


async def update_game_service(session: AsyncSession, game_id: int, data: GameUpdate, user_id: int) -> GameOut:
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


async def delete_game_service(session: AsyncSession, game_id: int, user_id: int) -> dict:
    game = await GameRepository.get_by_id(session, game_id)
    if not game:
        raise GameNotFound(game_id)

    if game.owner_id != user_id:
        raise PermissionDenied("You cannot delete this game")

    await GameRepository.delete(session, game)
    return {"id": game_id, "message": f"Game '{game.name}' deleted successfully"}


async def get_game_info_service(session: AsyncSession, game_id: int) -> GameOut:
    game = await GameRepository.get_by_id(session, game_id)
    if not game:
        raise GameNotFound(game_id)
    return GameOut.model_validate(game)
