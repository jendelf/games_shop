from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.types import JSON
import enum
from typing import List
from src.auth.models import User

class GameGenre(str, enum.Enum):
    FANTASY = "fantasy"
    THRILLER = "thriller"
    #TODO дописать возможные жанры книг


class Game(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    genre: Mapped[GameGenre] = mapped_column(String, nullable=False)
    photos_url: Mapped[List[str] | None] = mapped_column(JSON, nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="items")    
   #TODO отредактировать класс согласно датасету с хагинфейса

class Cart():
    pass

class Order():
    pass

class Balance():
    pass