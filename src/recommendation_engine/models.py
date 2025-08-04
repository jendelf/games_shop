from src.database import Base

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class GameSimilarity(Base):

    from_game_id = Column(Integer, ForeignKey("games.appid"), primary_key=True)
    to_game_id = Column(Integer, ForeignKey("games.appid"), primary_key=True)
    similarity_score = Column(Float, nullable=False)

    from_game = relationship("Game", foreign_keys=[from_game_id], back_populates="similar_to")
    to_game = relationship("Game", foreign_keys=[to_game_id], back_populates="similar_from")