import aiohttp

async def fetch_json(url: str) -> dict:
    """
    Запрашивает JSON по указанному URL.
    :param url: URL для запроса.
    :return: JSON-ответ.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Ошибка при запросе JSON: {response.status}")

async def check_image_exists(url: str) -> bool:
    """
    Проверяет, существует ли изображение по указанному URL.
    :param url: URL изображения.
    :return: True, если изображение существует, иначе False.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response.status == 200