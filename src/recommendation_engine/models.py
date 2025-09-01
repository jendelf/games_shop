
from __future__ import annotations
from typing import TYPE_CHECKING

from src.database import Base

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

if TYPE_CHECKING:
    from src.shop.models import Game
    from src.auth.models import User


class GameSimilarity(Base):
    from_game_id = Column(Integer, ForeignKey("games.appid"), primary_key=True)
    to_game_id = Column(Integer, ForeignKey("games.appid"), primary_key=True)
    similarity_score = Column(Float, nullable=False)

    from_game = relationship("Game", foreign_keys=[from_game_id], back_populates="similar_to")
    to_game = relationship("Game", foreign_keys=[to_game_id], back_populates="similar_from")


class Recommendation(Base):
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "game_id"),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.appid"))

    score: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="recommendations")
    game: Mapped["Game"] = relationship("Game")