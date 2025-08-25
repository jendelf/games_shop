import asyncio
import aiohttp
from datetime import datetime
from sqlalchemy import select
from src.shop.models import Game
from src.database import async_session_maker

STEAM_API_URL = "https://store.steampowered.com/api/appdetails"

async def update_game(session_db, appid: int):
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(STEAM_API_URL, params={"appids": appid, "cc": "us", "l": "en"}) as resp:
                data = await resp.json(content_type=None)

        game_data = data.get(str(appid), {}).get("data")
        if not game_data:
            print(f"No data for appid {appid}")
            return False

        result = await session_db.execute(select(Game).where(Game.appid == appid))
        game = result.scalars().first()
        if not game:
            game = Game(appid=appid, name=game_data.get("name", f"Game {appid}"))
            session_db.add(game)

        # Обновляем поля
        game.name = game_data.get("name", game.name)
        game.short_description = game_data.get("short_description", "")
        game.detailed_description = game_data.get("detailed_description") or game_data.get("about_the_game", "")
        game.image_url = game_data.get("header_image", game.image_url)
        rd = game_data.get("release_date", {}).get("date")
        if rd:
            try:
                # Преобразуем в datetime.date
                game.release_date = datetime.strptime(rd, "%b %d, %Y").date()
            except ValueError:
                game.release_date = None
        game.developer = ", ".join(game_data.get("developers", [])) or game.developer
        game.genres = ", ".join([g.get("description", "") for g in game_data.get("genres", [])]) or game.genres
        game.platforms = ", ".join([k for k,v in game_data.get("platforms", {}).items() if v]) or game.platforms
        if price := game_data.get("price_overview"):
            game.price = price.get("final", game.price) / 100.0

        await session_db.commit()
        print(f"Game {game.name} ({appid}) updated successfully.")
        return True

    except Exception as e:
        await session_db.rollback()
        print(f"Error updating game {appid}: {e}")
        return False

async def update_all_games(limit=1000):
    async with async_session_maker() as session_db:
        result = await session_db.execute(select(Game.appid).limit(limit))
        appids = [row[0] for row in result.all()]

    print(f"Updating {len(appids)} games from Steam safely...")

    for appid in appids:
        await update_game(session_db, appid)

if __name__ == "__main__":
    asyncio.run(update_all_games())
