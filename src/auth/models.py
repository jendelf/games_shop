from sqlalchemy import String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.role import Role

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.shop.models import Game, Cart, Recommendation, Order

class User(Base):
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String,nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    balance: Mapped[float]
    role: Mapped[Role] = mapped_column(SQLEnum(Role, name="role_enum"), default=Role.CUSTOMER, nullable=False)
    items: Mapped[List["Game"]] = relationship(back_populates="owner")
    cart_items: Mapped[List["Cart"]] = relationship("Cart", back_populates="owner") 
    recommendations: Mapped[List["Recommendation"]] = relationship(back_populates="user")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")

class RefreshToken(Base):
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

