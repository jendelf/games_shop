from .models import Cart, Game
from src.auth.models import User
from src.database import async_session_maker
from sqlalchemy import select
from.schemas import CartBase

class CartRepository:
    @classmethod
    async def add_to_cart(cls, quantity, game_id: int, user_id: int):
        query = select(user_i