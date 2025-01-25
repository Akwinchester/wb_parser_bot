from parser.requests import fetch_json, check_image_exists


def generate_product_url(article: str, host: str) -> str:
    """
    Генерирует URL для запроса данных о товаре.
    :param article: Артикул товара.
    :param host: Хост для формирования URL.
    :return: Сформированный URL.
    """
    article_length = len(article)

    if article_length >= 9:
        vol_part = article[:4]
        part_part = article[:6]
    elif article_length == 8:
        vol_part = article[:3]
        part_part = article[:5]
    elif article_length == 7:
        vol_part = article[:2]
        part_part = article[:4]
    elif article_length == 6:
        vol_part = article[:1]
        part_part = article[:3]

    return f"https://{host}/vol{vol_part}/part{part_part}/{article}/info/ru/card.json"


async def fetch_product_data(article: str, host: str) -> dict:
    """
    Запрашивает данные о товаре по артикулу.
    :param article: Артикул товара.
    :param host: Хост для запроса.
    :return: Данные о товаре.
    """
    product_url = generate_product_url(article, host)
    return await fetch_json(product_url)


async def fetch_image_urls(base_url: str) -> list:
    """
    Получает список ссылок на изображения товара.
    :param base_url: Базовый URL для формирования ссылок на изображения.
    :return: Список доступных ссылок на изображения.
    """
    image_urls = []
    image_number = 1

    while True:
        image_url = f"{base_url}/images/big/{image_number}.webp"
        if await check_image_exists(image_url):
            image_urls.append(image_url)
            image_number += 1
        else:
            break

    return image_urls


async def fetch_additional_data(article: str) -> dict:
    """
    Запрашивает дополнительные данные о товаре (цена, рейтинг, отзывы).
    :param article: Артикул товара.
    :return: Дополнительные данные о товаре.
    """
    detail_url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1255576&spp=30&hide_dtype=10&ab_testing=false&nm={article}"
    detail_data = await fetch_json(detail_url)
    product = detail_data.get("data", {}).get("products", [{}])[0]

    return {
        "price_total": product.get("sizes", [{}])[0].get('price', {}).get('total', 0) / 100,
        "supplier_rating": product.get("reviewRating", 0),
        "feedbacks": product.get("feedbacks", 0),
    }


def transform_product_data(raw_data: dict) -> dict:
    """
    Преобразует исходный JSON в требуемый формат product_data.
    :param raw_data: Исходный JSON с данными о товаре.
    :return: Преобразованный словарь product_data.
    """
    name = raw_data.get("imt_name", "Название не указано")
    category = raw_data.get("subj_root_name", "Категория не указана")
    description = raw_data.get("description", "Описание не указано")
    images = raw_data.get("imgs", [])
    price_total = raw_data.get("price_total", 0)
    supplier_rating = raw_data.get("supplier_rating", 0)
    feedbacks = raw_data.get("feedbacks", 0)

    attributes = {option.get("name", ""): option.get("value", "") for option in raw_data.get("options", [])}

    return {
        "name": name,
        "category": category,
        "price": price_total,
        "rating": supplier_rating,
        "reviews": feedbacks,
        "description": description,
        "images": images,
        "attributes": attributes
    }
