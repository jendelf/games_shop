from pydantic import BaseModel, ConfigDict, Field
from .models import GameGenre

class PaginationParams(BaseModel):
    limit: int
    offset: int 
    sort_by: str | None=None
    search: str | None=None

class GameBase(BaseModel):
    name: str
    genre: GameGenre
    price: float
    description: str | None = None
    photos_url: list[str]

class GameCreate(GameBase):
    pass

class GameOut(GameCreate):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

class GameUpdate(GameCreate):
    name: str | None = None 
    genre: GameGenre | None = None 
    price: float | None = None 
    description: str | None = None
    photos_url: list[str] | None = None 

class CartBase(BaseModel):
    game_id: int = Field(..., description = "game id added to cart")
    quantity: int = Field(..., description = "Number of items")

class CartAddItem(CartBase):
    pass
