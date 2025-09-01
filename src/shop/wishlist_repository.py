from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .models import Wishlist, Game
from .schemas import PageParams
from typing import List

class WishlistRepository:
    @classmethod
    async def add_to_wishlist(cls, session: AsyncSession, game_id: int, wishlist: Wishlist) -> Wishlist:
        game = await session.get(Game, game_id)
        if not game:
            raise ValueError(f"Game with id {game_id} not found")
        wishlist.games.append(game)
        await session.commit()
        return wishlist
    
    @classmethod
    async def delete_from_wishlist(cls, session: AsyncSession, game_id: int, wishlist_id: int) -> Wishlist:
        wishlist = await session.get(Wishlist, wishlist_id)
        if not wishlist:
            raise ValueError(f"Wishlist with id {wishlist_id} not found")
        game_to_remove = next((g for g in wishlist.games if g.appid == game_id), None)
        if game_to_remove:
            wishlist.games.remove(game_to_remove)
        await session.commit()
        return wishlist
    
    @staticmethod
    async def get_wishlist_paginated(session: AsyncSession, wishlist_id: int, pagination: PageParams) -> list[Game]:
        query = (
            select(Game)
            .join(Wishlist.games)
            .where(Wishlist.id == wishlist_id)
            .order_by(Game.name.desc())
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def count_all(session: AsyncSession, wishlist_id: int) -> int:
        query = (
            select(func.count(Game.appid))
            .join(Wishlist.games)
            .where(Wishlist.id == wishlist_id)
        )
        result = await session.execute(query)
        return result.scalar()