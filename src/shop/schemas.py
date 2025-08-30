from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
class PageParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    @property
    def limit(self) -> int:
        return self.page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

class IdSchema(BaseModel):
    id: int = Field(..., description="ID of the object")

class GameBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)
    image_url: str | None = None

class GameCreate(GameBase):
    pass

class GameOut(GameBase):
    appid: int
    name: str
    price: float
    image_url: Optional[str] = None
    photos_url: Optional[List[str]] = None
    description: Optional[str] = None
    detailed_description: Optional[str] = None
    short_description: Optional[str] = None
    model_config = {
        "from_attributes": True
    }
class GameUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=500)
    photos_url: Optional[List[str]] = None

class CartBase(BaseModel):
    game_id: int = Field(..., description="game id added to cart")
    quantity: int = Field(..., description="Number of items")
    user_id: int = Field(..., description="owner id")
    model_config = ConfigDict(from_attributes=True)


class CartOut(CartBase):
    user_id: int
    game: GameBase
    model_config = ConfigDict(from_attributes=True)

class OrderItemBase(BaseModel):
    game_id: int = Field(..., description="game in the order")
    quantity: int = Field(..., description="number of copies")

class OrderCreate(BaseModel):
    items: list[OrderItemBase]

class OrderOut(BaseModel):
    id: int
    user_id: int
    created_at: str
    total_price: float
    model_config = ConfigDict(from_attributes=True)

class PaginatedResponse(BaseModel):
    games: List[GameOut]
    total: int
    page: int
    page_size: int
    total_pages: int