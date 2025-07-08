from fastapi import FastAPI
from auth.router import router as auth_router
from shop.router import router as shop_router
import uvicorn

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(shop_router, prefix="/shop", tags=["shop"])

if __name__ == "__main__":
    uvicorn.run ("main:app", reload=True)