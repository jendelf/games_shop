from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .models import Game
from .schemas import PageParams
from typing import List

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

    @staticmethod
    async def get_paginated(session: AsyncSession, limit: int, offset: int) -> List[Game]:
        query = await session.execute(
            select(Game)
            .order_by(Game.positive_ratings.desc())
            .limit(limit)
            .offset(offset)
        )
        return query.scalars().all()

    @staticmethod
    async def count_all(session: AsyncSession) -> int:
        query = await session.execute(select(func.count()).select_from(Game))
        return query.scalar()
    

    #TODO тут нужно просмотреть где-то изменить classmethod на staticmethod, функцию count_all привести к виду как в wishlist repository