import re
from parser.upstreams import get_host_for_article
from parser.utils import fetch_product_data, generate_product_url, fetch_image_urls, \
    fetch_additional_data, transform_product_data
from my_logging_package import Logger

logger_error = Logger(name="logger_error", log_file='error').get_logger()

def validate_article(article: str) -> bool:
    """Проверяет, соответствует ли артикул заданному формату."""
    return bool(re.match(r"^\d{6,10}$", article))

async def parse_wildberries_product(article: str):
    """Основная функция для парсинга товара с Wildberries."""
    try:
        host = await get_host_for_article(article)
        product_data = await fetch_product_data(article, host)

        base_image_url = generate_product_url(article, host).replace("/info/ru/card.json", "")
        product_data["imgs"] = await fetch_image_urls(base_image_url)

        additional_data = await fetch_additional_data(article)
        product_data.update(additional_data)

        return transform_product_data(product_data)

    except Exception as e:
        logger_error.error(f"Ошибка при парсинге артикула {article}: {e}")
        return None
