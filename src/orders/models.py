from __future__ import annotations
from typing import TYPE_CHECKING, List

from src.database import Base, TimestampedBase

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

if TYPE_CHECKING:
    from src.shop.models import Game
    from src.auth.models import User

class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.appid"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_at_purchase: Mapped[float] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="games")
    game: Mapped["Game"] = relationship("Game", back_populates="order_items")


class Order(TimestampedBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total_price: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="orders")
    games: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")