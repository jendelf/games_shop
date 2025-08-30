from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .models import Game
from .schemas import PageParams


class GameRepository:
    @classmethod
    async def add(cls, session: AsyncSession, game: Game) -> Game:
        session.add(game)
        await session.commit()
        await session.refresh(game)
        return game

    @classmethod
    async def get_by_id(cls, session: AsyncSession, game_id: int) -> Game | None:
        result = await session.execute(select(Game).where(Game.appid == game_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_by_title(cls, session: AsyncSession, title: str) -> Game | None:
        result = await session.execute(select(Game).where(Game.name == title))
        return result.scalar_one_or_none()

    @classmethod
    async def update(cls, session: AsyncSession, game: Game) -> Game:
        await session.commit()
        await session.refresh(game)
        return game

    @classmethod
    async def delete(cls, session: AsyncSession, game: Game) -> None:
        await session.delete(game)
        await session.commit()

    @classmethod
    async def list_paginated(cls, session: AsyncSession, pagination: PageParams) -> list[Game]:
        query = select(Game).offset(pagination.offset).limit(pagination.page_size)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def count_items(cls, session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(Game))
        return result.scalar()

    @classmethod
    async def set_game_image(cls, session: AsyncSession, game: Game, image_url: str) -> Game:
        game.image_url = image_url
        session.add(game)
        await session.commit()
        await session.refresh(game)
        return game
