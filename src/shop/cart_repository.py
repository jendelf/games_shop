from .models import Cart, Game
from src.auth.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from.schemas import CartBase
from .exceptions import GameNotFound

class CartRepository:
    @classmethod
    async def add_to_cart(cls, quantity: int, game_id: int, user_id: int, session: AsyncSession):
        existing_result = await session.execute(select(Cart).where(Cart.owner_id == user_id, Cart.game_id == game_id)) 
        existing_item = existing_result.scalar_one_or_none()
        
        if existing_item:
            existing_item.games_quantity += quantity
        else:
            game_result = await session.execute(select(Game).where(Game.appid == game_id))
            game = game_result.scalar_one_or_none()
            if not game:
                raise GameNotFound(game_id)
            new_item = Cart(owner_id=user_id, game_id=game_id, games_quantity=quantity)
            session.add(new_item)
        await session.commit()
                

        
