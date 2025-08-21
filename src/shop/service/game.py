from sqlalchemy.ext.asyncio import AsyncSession
from src.shop.game_repository import GameRepository
from src.shop.schemas import PageParams, GameCreate, GameOut, GameUpdate
from typing import List
from .steam_api import fetch_steam_image
from src.shop.models import Game
from sqlalchemy import select, desc


async def get_paginated_games(session: AsyncSession, pagination) -> List[GameOut]:
    query = await session.execute(
        select(Game)
        .order_by(Game.positive_ratings.desc())
        .limit(pagination.limit)
        .offset(pagination.offset)
    )
    games: List[Game] = query.scalars().all()
    
    print(f"=== ОТЛАДКА: Найдено {len(games)} игр ===")
    
    for game in games:
        print(f"Игра: {game.name}")
        print(f"  appid: {game.appid}")
        print(f"  image_url в базе: {repr(game.image_url)}")  # repr покажет None или пустую строку
        print(f"  Условие not game.image_url: {not game.image_url}")
        
        if not game.image_url:
            print(f"  ⚡ ГЕНЕРИРУЮ URL для {game.name}...")
            image_url = await fetch_steam_image(game.appid)
            print(f"  ⚡ Сгенерирован URL: {image_url}")
            if image_url:
                game.image_url = image_url
                session.add(game)
        else:
            print(f"  ⏭️  У игры уже есть image_url, пропускаю")
        print("---")
    
    await session.commit()

    return [
        GameOut.model_validate({
            **game.__dict__,
            "image_url": game.image_url
        }) for game in games
    ]

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
