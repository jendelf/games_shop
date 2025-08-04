import pandas as pd
import re
from src.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import async_session_maker
from src.shop.models import Game
import asyncio
def preprocess_text(text: str) -> str:
    text = str(text).lower()
    return re.sub(r"[^\w\s]", "", text)

def recommendation_df_preprocess() -> pd.DataFrame:

    recom_df = pd.read_csv(settings.RAW_DATA / "steam.csv")
    recom_df.columns = recom_df.columns.str.strip()

    columns_to_drop_recommender = [
        "publisher", "english", "platforms", "required_age",
        "achievements", "average_playtime",
        "median_playtime", "owners"
    ]
    
    recom_df = recom_df.drop(columns=[col for col in columns_to_drop_recommender if col in recom_df.columns])

    # delete duplicates and fill NaN values
    recom_df = recom_df.drop_duplicates()
    recom_df[['genres', 'steamspy_tags', 'developer']] = recom_df[['genres', 'steamspy_tags', 'developer']].fillna('')

    # combine and preprocess
    recom_df['processed_text'] = (recom_df['genres'] + " " + recom_df['steamspy_tags']).apply(preprocess_text)

    #save processed data in a csv file
    recom_df.to_csv(settings.PROCESSED_DATA / "steam_data_processed.csv", index=False)
    return recom_df


async def shop_df_preprocess() -> pd.DataFrame:
    shop_df = pd.read_csv(settings.RAW_DATA / "steam.csv")

    columns_to_drop_shop = [
        "publisher", "english", "achievements", "median_playtime", "owners"
    ]
    shop_df = shop_df.drop(columns=[col for col in columns_to_drop_shop if col in shop_df.columns])

    shop_df = shop_df.fillna('')
    shop_df['release_year'] = pd.to_datetime(shop_df['release_date'], errors='coerce').dt.year
    shop_df['price'] = pd.to_numeric(shop_df['price'], errors='coerce').fillna(0.0)
    shop_df['platforms'] = shop_df['platforms'].str.lower().str.strip()

    for col in ['genres', 'steamspy_tags', 'name']:
        shop_df[col] = shop_df[col].astype(str).apply(preprocess_text)

    return shop_df

async def import_games_from_df(session: AsyncSession, df: pd.DataFrame):
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').dt.date

    for _, row in df.iterrows():
        game = Game(
            appid=int(row["appid"]),
            name=row["name"],
            release_date=row["release_date"],
            platforms=row["platforms"],
            developer=row["developer"],
            categories=row["categories"],
            genres=row["genres"],
            steamspy_tags=row["steamspy_tags"],
            required_age=int(row["required_age"]),
            positive_ratings=int(row["positive_ratings"]),
            negative_ratings=int(row["negative_ratings"]),
            average_playtime=int(row["average_playtime"]),
            price=float(row["price"]),
            owner_id=None
        )
        session.add(game)

    await session.commit()

async def main():
    df = await shop_df_preprocess()
    async with async_session_maker() as session:
        await import_games_from_df(session, df)

if __name__ == "__main__":
    asyncio.run(main())