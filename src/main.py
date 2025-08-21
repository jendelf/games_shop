from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from src.auth.router import router as auth_router
from src.shop.router import router as shop_router
from src.recommendation_engine.router import router as recommendation_router 
from src.cors import setup_cors
from src.settings import STATIC_PATH
from src.auth.create_admin import create_admin_user
from .database import async_session_maker

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_session_maker() as session:
        await create_admin_user(session)
    yield

app = FastAPI(lifespan=lifespan)
setup_cors(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API роуты
app.include_router(auth_router, prefix="/api/auth")
app.include_router(shop_router, prefix="/api/shop")
app.include_router(recommendation_router, prefix="/api/recommendations")

# Статические файлы (CSS, JS, изображения)
app.mount("/css", StaticFiles(directory=STATIC_PATH / "css"), name="css")
app.mount("/js", StaticFiles(directory=STATIC_PATH / "js"), name="js")
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

# SPA fallback (должен быть ПОСЛЕДНИМ!)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Если запрос к API, возвращаем 404
    if full_path.startswith("api"):
        return {"detail": "Not Found"}
    
    # Если запрос к статическим файлам, пропускаем
    if full_path.startswith(("css/", "js/", "images/", "static/")):
        return {"detail": "Not Found"}
    
    # Иначе возвращаем index.html для SPA
    return FileResponse(STATIC_PATH / "index.html")