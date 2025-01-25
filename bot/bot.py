from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from bot.utils import authorized_only, AuthState, load_user_data, save_user_data
from config import BOT_TOKEN, SHEET_ID, SHEET_NAME, INSTRUCTION_BOT, PASSWORD_BOT
from google_api.google_sheets import append_or_update_sheet, export_google_sheet_to_csv
from my_logging_package import Logger
from parser.parser import parse_wildberries_product
from aiogram.fsm.storage.memory import MemoryStorage

# Инициализация бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

logger_error = Logger(name="logger_error", log_file='error').get_logger()

storage = MemoryStorage()  # Хранилище для состояний
dp = Dispatcher(storage=storage)  # Передаем хранилище в диспетчер
router = Router()

# Обработчик команды /start и /inf
@router.message(Command(commands=["start", "inf"]))
@authorized_only()
async def get_inf(message: Message):
    """Обрабатывает команды /start и /inf."""
    await message.answer(INSTRUCTION_BOT)

# Обработчик для парсинга данных по артикулу
@router.message(lambda message: message.text.isdigit())
@authorized_only()
async def parse_article_handler(message: Message):
    """Парсит данные товара по артикулу и сохраняет в Google Sheets."""
    article = message.text
    await message.answer(f'Обрабатываю артикул {article}')
    try:
        data = await parse_wildberries_product(article)
        if data is None:
            await message.answer("Ошибка: не удалось обработать запрос.")
        sheet_data = [
            [
                article,
                data["name"],
                data["category"],
                data["price"],
                data["rating"],
                data["reviews"],
                data["description"],
                ", ".join(data["images"]),
                str(data["attributes"]),
            ]
        ]
        response = (
            f"📦 <b>Товар:</b> {data['name']}\n"
            f"🛒 <b>Категория:</b>  {data['category']}\n"
            f"💰 <b>Цена:</b>  {data['price']} ₽\n"
            f"⭐️ <b>Рейтинг:</b>  {data['rating']} ({data['reviews']} отзывов)\n"
            f"📜 <b>Описание:</b> \n {data['description']}\n\n"
            f"🔍 <b>Характеристики:</b> \n {data['attributes']}\n\n"
            f"🖼 <b>Изображения:</b>  {', '.join(data['images'])}"
        )
        await message.answer(response)

        google_sheet_status = await append_or_update_sheet(SHEET_ID, SHEET_NAME, sheet_data)

        if google_sheet_status:
            await message.answer("Данные в google-таблице успешно актуализированы")
        else:
            await message.answer("Ошибка при актуализации google-таблицы")
    except Exception as e:
        await message.answer("Ошибка: не удалось обработать запрос.")
        print(e)

# Обработчик для экспорта Google Sheets в CSV
@router.message(Command(commands=["exp"]))
@authorized_only()
async def export_handler(event: Message):
    """Экспортирует данные Google Sheets в CSV и отправляет файл."""
    try:
        # Экспортируем данные Google Sheets в CSV
        file_path = await export_google_sheet_to_csv(SHEET_ID, SHEET_NAME)

        # Отправляем CSV файл пользователю
        file = FSInputFile(file_path)
        await event.answer_document(file)
    except Exception as e:
        # Обработка ошибок
        await event.answer("Ошибка экспорта данных.")
        print(f"Ошибка экспорта: {e}")

@router.message(AuthState.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    """
    Обрабатывает ввод кодовой фразы для авторизации.
    """
    chat_id = message.chat.id

    if message.text == PASSWORD_BOT:
        # Если кодовая фраза верна, авторизуем пользователя
        data = load_user_data()
        data['login'].append(chat_id)
        save_user_data(data)
        await message.answer("Вы успешно авторизовались.")
        await message.answer(INSTRUCTION_BOT)
        # Сбрасываем состояние
        await state.clear()
    else:
        # Если кодовая фраза неверна, просим ввести снова
        await message.answer("Неверная кодовая фраза. Попробуйте снова.")

# Эхо-обработчик
@router.message()
@authorized_only()
async def fallback_handler(message: Message):
    """Обрабатывает неподдерживаемые сообщения."""
    await message.answer("Команда не распознана. Используйте /start или введите артикул.")

# Регистрация роутера в диспетчере
dp.include_router(router)
