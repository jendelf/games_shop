from pydantic_settings import BaseSettings
from pathlib import Path

ENV_PATH = Path(__file__).parent / ".env"

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    ADMIN_USERNAME: str
    DATABASE_URL: str
    
    class Config:
        env_file = ENV_PATH

settings = Settings()