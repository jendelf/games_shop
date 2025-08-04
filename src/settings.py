from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import List, Tuple

BASE_DIR = Path(__file__).resolve().parent
STATIC_PATH = BASE_DIR / "static"
SRC_DIR = Path(__file__).resolve().parent
ENV_PATH = SRC_DIR.parent / ".env"
DATA_PATH = SRC_DIR / "data"
MODEL_PATH = SRC_DIR / "model"

class Settings(BaseSettings):
#config to create JWT
#---------------------------------------------------------------------------------------------
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"

#config to create admin acc
#---------------------------------------------------------------------------------------------
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    ADMIN_USERNAME: str

#db and list of domens for frontend
#---------------------------------------------------------------------------------------------
    DATABASE_URL: str

    CORS_ORIGINS: List[str] = ["*"]  # TODO: добавить список доменов для фронта

#pathes to data and matrices
#---------------------------------------------------------------------------------------------
    RAW_DATA: Path = DATA_PATH / "unfiltered" 
    PROCESSED_DATA: Path = DATA_PATH / "filtered" 
    MODEL_DIR: Path = MODEL_PATH

#TI-IDF params
#---------------------------------------------------------------------------------------------
    MAX_FEATURES: int = 1500
    NGRAM_RANGE: Tuple[int, int] = (1, 2)

    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8")

settings = Settings()
