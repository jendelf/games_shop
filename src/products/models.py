from sqlalchemy.orm import Mapped, mapped_column
from database import Base

#TODO придумать что будет продаваться
class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    #TODO Прописать модель с товарами
