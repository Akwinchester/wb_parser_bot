from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Константы конфигурации
PASSWORD_BOT = os.environ.get('PASSWORD_BOT')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
SHEET_ID = os.environ.get('SHEET_ID')
SHEET_NAME = os.environ.get('SHEET_NAME')
USERS_FILE = './users.json'
SERVICE_ACCOUNT_FILE = 'credentials/service_account.json'


INSTRUCTION_BOT = '''
<b>Получение информации о товаре:</b>

Отправьте боту артикул товара на Wildberries (например, <code>256320324</code>).
Бот проверит валидность введенного артикула, спарсит данные карточки товара и вернет:
- Артикул товара
- Название товара
- Категорию
- Цена
- Ссылки на изображения (список)
- Характеристики в формате JSON
- Описание
- Рейтинг
- Количество отзывов

<b>Сохранение данных в Google-таблицу:</b>

- Данные по каждому новому артикулу сохраняются в Google-таблицу в новую строку.
- Если артикул уже существует, данные обновляются.

<b>Экспорт данных:</b>

- Команда <code>/exp</code> позволяет экспортировать данные из Google-таблицы в CSV-файл, который бот отправит вам.

<b>Уведомления об ошибках:</b>

- В случае недоступности Wildberries или Google API, а также при вводе некорректного артикула, бот уведомит вас об ошибке.
'''
