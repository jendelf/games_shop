from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from pathlib import Path

from .auth.router import router as auth_router
from .shop.router import router as shop_router
from .recommendation_engine.router import router as recommendation_router  

app = FastAPI()

# CORS — если frontend работает отдельно
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на проде обязательно укажи конкретный origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth")
app.include_router(shop_router, prefix="/api/shop")
app.include_router(recommendation_router, prefix="/api/recommendations")

# Раздача frontend
static_path = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if full_path.startswith("api"):
        return {"detail": "Not Found"}
    return FileResponse(static_path / "index.html")