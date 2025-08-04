from pydantic import BaseModel, ConfigDict, Field

class PageParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

class GameBase(BaseModel):
    name: str
    price: float
    description: str | None=None
    photos_url: list[str]

class GameCreate(GameBase):
    pass

class GameOut(GameCreate):
    id: int
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

class GameUpdate(GameCreate):
    name: str | None=None 
    price: float | None=None 
    description: str | None=None
    photos_url: list[str] | None=None 

class CartBase(BaseModel):
    game_id: int = Field(..., description="game id added to cart")
    quantity: int = Field(..., description="Number of items")

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
