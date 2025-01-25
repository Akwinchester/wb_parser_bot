import asyncio
import logging
from bot.bot import dp, bot

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    """
    Основная функция для запуска бота.
    """
    logging.info("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
