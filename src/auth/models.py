from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.shop.models import Game

class User(Base):
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String,nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    balance: Mapped[float]
    items: Mapped[list["Game"]] = relationship(back_populates="owner")


#TODO создать роли
