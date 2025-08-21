import aiohttp

async def fetch_steam_image(appid: int) -> str | None:
    image_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.head(image_url) as resp:
                if resp.status == 200:
                    return image_url
        except Exception:
            pass
    
    return None