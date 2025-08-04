from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.auth.router import router as auth_router
from src.shop.router import router as shop_router
from src.recommendation_engine.router import router as recommendation_router 
from src.cors import setup_cors
from src.settings import STATIC_PATH

app = FastAPI()
setup_cors(app)

app.include_router(auth_router, prefix="/api/auth")
app.include_router(shop_router, prefix="/api/shop")
app.include_router(recommendation_router, prefix="/api/recommendations")

app.mount("/", StaticFiles(directory=STATIC_PATH, html=True), name="static")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if full_path.startswith("api"):
        return {"detail": "Not Found"}
    return FileResponse(STATIC_PATH / "index.html")