from database import new_session
from .models import Game
from .schemas import GameCreate, GameOut, GameUpdate
from sqlalchemy import select
from .exceptions import GameNotFound, GameAlreadyExist


class GameRepository:
    @classmethod
    async def add_game(cls, game_title: str, data: GameCreate) -> GameOut:  #Add new game to the shop
        async with new_session() as session:
            query = select(Game).where(Game.name == game_title)
            result = await session.execute(query)
            game_model = result.scalar_one_or_none()
            if game_model is not None:
                raise GameAlreadyExist(game_title) 
            game_dict = data.model_dump()
            game = Game(**game_dict)
            session.add(game)
            await session.flush()
            await session.commit()
            return GameOut.model_validate(game)
        
    @classmethod
    async def get_all(cls) -> list[GameOut]: # Retrieve all games from DB 
        async with new_session() as session:
            query = select(Game)
            result = await session.execute(query)
            game_models = result.scalars().all()
            game_schemas = [GameOut.model_validate(game_model) for game_model in game_models]
            return game_schemas
    @classmethod
    async def update_game(cls, game_id: int, data: GameUpdate) -> GameOut: #Update information about the game
        async with new_session() as session:
            query = select(Game).where(Game.id == game_id) 
            result = await session.execute(query)
            game = result.scalar_one_or_none()
            if game is None:
                raise GameNotFound(game_id)
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items(): # Automatically change parameters that came from the client
                setattr(game, key, value)
            await session.refresh(game)
            await session.commit()
            return GameOut.model_validate(game)
    @classmethod
    async def delete_game(cls, game_id) -> str:
        async with new_session() as session:
            query = select(Game).where(Game.id == game_id)
            result = await session.execute(query)
            game = result.scalar_one_or_none()
            if game is None:
                raise GameNotFound(game_id)
            await session.delete(game)
            await session.commit()
            return {f"Game '{game.name}' was successfully deleted!"}
    






