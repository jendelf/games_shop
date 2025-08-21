from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .models import Game
from .schemas import GameCreate, GameOut, GameUpdate, PageParams
from .exceptions import GameNotFound, GameAlreadyExist
from src.database import async_session_maker

class GameRepository:
    @classmethod
    async def add_game(cls, game_title: str, data: GameCreate) -> GameOut:
        async with async_session_maker() as session:
            query = select(Game).where(Game.name == game_title)
            result = await session.execute(query)
            game_model = result.scalar_one_or_none()
            if game_model:
                raise GameAlreadyExist(game_title)
            game = Game(**data.model_dump())
            session.add(game)
            await session.flush()
            await session.commit()
            return GameOut.model_validate(game)

    @classmethod
    async def update_game(cls, game_id: int, data: GameUpdate) -> GameOut:
        async with async_session_maker() as session:
            query = select(Game).where(Game.id == game_id)
            result = await session.execute(query)
            game = result.scalar_one_or_none()
            if game is None:
                raise GameNotFound(game_id)
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(game, key, value)
            await session.commit()
            await session.refresh(game)
            return GameOut.model_validate(game)

    @classmethod
    async def delete_game(cls, game_id: int) -> dict:
        async with async_session_maker() as session:
            query = select(Game).where(Game.id == game_id)
            result = await session.execute(query)
            game = result.scalar_one_or_none()
            if game is None:
                raise GameNotFound(game_id)
            await session.delete(game)
            await session.commit()
            return {"message": f"Game '{game.name}' was successfully deleted!"}

    @classmethod
    async def get_items_with_pagination(cls, session: AsyncSession, pagination: PageParams):
        query = select(Game).offset(pagination.offset).limit(pagination.page_size)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def count_items(cls, session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(Game))
        return result.scalar()

    @classmethod
    async def set_game_image(cls, game: Game, image_url: str, session: AsyncSession):
        game.image_url = image_url
        session.add(game)
        await session.commit()
        await session.refresh(game)
        return game



