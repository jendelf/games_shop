from fastapi import FastAPI
from auth.auth_router import router as auth_router
from products.products_router import router as products_router
import uvicorn

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(products_router, prefix="/products", tags=["products"])

if __name__ == "__main__":
    uvicorn.run ("main:app", reload=True)