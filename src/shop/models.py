from src.database import Base, TimestampedBase
from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql import func
from typing import List
from src.auth.models import User
from src.recommendation_engine.models import GameSimilarity
from sqlalchemy import Text

class Game(Base):
    appid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    image_url: Mapped[str] = mapped_column(nullable=True) 

    release_date: Mapped[date | None] = mapped_column(nullable=True)
    platforms: Mapped[str] = mapped_column(default="windows")
    developer: Mapped[str] = mapped_column(default="", nullable=False)

    categories: Mapped[str] = mapped_column(default="", nullable=False)
    genres: Mapped[str] = mapped_column(default="", nullable=False)
    steamspy_tags: Mapped[str] = mapped_column(default="", nullable=False)

    required_age: Mapped[int] = mapped_column(default=0, nullable=False)

    positive_ratings: Mapped[int] = mapped_column(default=0, nullable=False)
    negative_ratings: Mapped[int] = mapped_column(default=0, nullable=False)
    average_playtime: Mapped[int] = mapped_column(default=0, nullable=False)

    price: Mapped[float] = mapped_column(default=0.0, nullable=False)

    short_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    detailed_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    owner: Mapped["User"] = relationship("User", back_populates="items", lazy="selectin")

    carts: Mapped[List["Cart"]] = relationship("Cart", back_populates="game")
    recommendations: Mapped[List["Recommendation"]] = relationship("Recommendation", back_populates="game")

    similar_to = relationship(
        "GameSimilarity",
        foreign_keys="GameSimilarity.from_game_id",
        back_populates="from_game",
        cascade="all, delete-orphan"
    )
    similar_from = relationship(
        "GameSimilarity",
        foreign_keys="GameSimilarity.to_game_id",
        back_populates="to_game",
        cascade="all, delete-orphan"
    )
    
class Cart(TimestampedBase):
    __table_args__ = (
        PrimaryKeyConstraint("owner_id", "game_id"),
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.appid"))

    quantity: Mapped[int] = mapped_column(nullable=True)
    
    owner: Mapped["User"] = relationship("User", back_populates="cart_items")
    game: Mapped["Game"] = relationship("Game", back_populates="carts")

class Recommendation(Base):
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "game_id"),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.appid"))

    score: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="recommendations")
    game: Mapped["Game"] = relationship("Game", back_populates="recommendations")

class OrderItem(Base):
    __table_args__ = (
        PrimaryKeyConstraint("order_id", "game_id"),
    )
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.appid"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_at_purchase: Mapped[float] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")
    game: Mapped["Game"] = relationship()


class Order(TimestampedBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total_price: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")