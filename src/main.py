from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from contextlib import asynccontextmanager
import uvicorn

from src.auth.create_admin import create_admin_user
from src.database import async_session_maker
from src.auth.router import router as auth_router
from src.shop.router import router as shop_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_maker() as session:
        await create_admin_user(session)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(shop_router, prefix="/shop", tags=["shop"])

app.mount("/static", StaticFiles(directory="src/auth/static"), name="static")
templates = Jinja2Templates(directory="src/auth/templates")

@app.get("/")
async def root():

    return RedirectResponse(url="/auth/login", status_code=302)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
