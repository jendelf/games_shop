from sqlalchemy import String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.role import Role

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.shop.models import Game

class User(Base):
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String,nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    balance: Mapped[float]
    role: Mapped[Role] = mapped_column(SQLEnum(Role, name="role_enum"), default=Role.CUSTOMER, nullable=False)
    items: Mapped[list["Game"]] = relationship(back_populates="owner")


class RefreshToken(Base):
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

