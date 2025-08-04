import pandas as pd
from src.settings import settings

from src.database import async_session_maker
from src.shop.models import Game

async def load_games_from_csv(df):
    df = pd.read_csv(settings.RAW_DATA)

    games = [Game(**row) for row in df.to_dict(orient="records")]

    async with async_session_maker() as session:
        session.add_all(games)
        await session.commit()