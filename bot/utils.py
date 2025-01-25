import json

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from config import PASSWORD_BOT, USERS_FILE

def load_user_data():
    """
    Загружает данные о пользователях из файла.

    :return: Словарь с данными о пользователях.
    """
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'login': []}

def save_user_data(data):
    """
    Сохраняет данные о пользователях в файл.

    :param data: Словарь с данными о пользователях.
    """
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f)

async def login_process(message: Message):
    """
    Обрабатывает процесс авторизации пользователя.

    :param message: Объект сообщения Telegram.
    """
    chat_id = message.chat.id
    if message.text == PASSWORD_BOT:
        data = load_user_data()
        data['login'].append(chat_id)
        save_user_data(data)
        await message.answer("Вы успешно авторизовались.")
    else:
        await message.answer("Неверная кодовая фраза. Попробуйте снова.")

class AuthState(StatesGroup):
    waiting_for_password = State()  # Состояние ожидания кодовой фразы

def authorized_only():
    """
    Декоратор для проверки авторизации пользователя.
    Если пользователь не авторизован, запрашивает кодовую фразу и переводит в состояние ожидания.
    """
    def decorator(handler):
        async def wrapper(event: Message, state: FSMContext, **kwargs):
            chat_id = event.chat.id
            authorized_users = load_user_data().get("login", [])

            if chat_id not in authorized_users:
                # Если пользователь не авторизован, запрашиваем кодовую фразу
                await event.answer("Привет! Введите кодовую фразу для авторизации.")
                # Устанавливаем состояние ожидания кодовой фразы
                await state.set_state(AuthState.waiting_for_password)
                return
            else:
                # Если пользователь авторизован, вызываем оригинальный обработчик
                return await handler(event)
        return wrapper
    return decorator