from datetime import datetime

from parser.utils import fetch_json


async def get_upstreams() -> list:
    """
    Получает список хостов для распределения запросов.
    :return: Список хостов.
    """
    current_time = int(datetime.now().timestamp() * 1000)
    upstreams_url = f"https://cdn.wbbasket.ru/api/v3/upstreams?t={current_time}"
    upstreams_data = await fetch_json(upstreams_url)
    return upstreams_data.get('recommend', {}).get("mediabasket_route_map", [])[0].get("hosts", [])

def calculate_article_prefix(article: str) -> int:
    """
    Определяет префикс артикула для выбора хоста.
    :param article: Артикул товара.
    :return: Префикс артикула.
    """
    article_length = len(article)

    if article_length >= 9:
        return int(article[:4])
    elif article_length == 8:
        return int(article[:3])
    elif article_length == 7:
        return int(article[:2])
    elif article_length == 6:
        return int(article[:1])
    else:
        raise ValueError("Некорректная длина артикула")

async def get_host_for_article(article: str) -> str:
    """
    Получает хост для указанного артикула.
    :param article: Артикул товара.
    :return: Хост для формирования URL.
    """
    hosts = await get_upstreams()
    article_prefix = calculate_article_prefix(article)

    for host_info in hosts:
        if host_info["vol_range_from"] <= article_prefix <= host_info["vol_range_to"]:
            return host_info["host"]

    raise Exception("Не удалось найти подходящий хост для артикула")