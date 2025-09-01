from __future__ import annotations

from sqlalchemy import Float, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import TimestampedBase
from src.role import Role

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.shop.models import Game, Cart, Wishlist
    from src.recommendation_engine.models import Recommendation
    from src.orders.models import Order

class User(TimestampedBase):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String,nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    role: Mapped[Role] = mapped_column(SQLEnum(Role, name="role_enum"), default=Role.CUSTOMER, nullable=False)

    #CONNECTIONS
#------------------------------------------------------------------------------------------------------------------
    games: Mapped[List["Game"]] = relationship(back_populates="owner")
    cart_games: Mapped[List["Cart"]] = relationship("Cart", uselist=False, back_populates="owner") 
    recommendations: Mapped[List["Recommendation"]] = relationship(back_populates="user")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")
    wishlist: Mapped["Wishlist"] = relationship("Wishlist", uselist=False, back_populates=None)

class RefreshToken(TimestampedBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

