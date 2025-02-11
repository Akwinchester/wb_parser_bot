# Telegram-бот для парсинга карточек Wildberries и интеграции с Google-таблицами

## Описание

Этот Telegram-бот позволяет получать информацию о товарах на Wildberries по их артикулу и сохранять данные в Google-таблицы. Бот также поддерживает экспорт данных в формате CSV.

## Функционал

1. **Получение информации о товаре**:
   - Отправьте боту артикул товара (например, `33441887`).
   - Бот проверяет корректность артикула и возвращает следующую информацию:
     - Артикул товара
     - Название товара
     - Категория
     - Цена
     - Ссылки на изображения (список)
     - Характеристики (в формате JSON)
     - Описание
     - Рейтинг
     - Количество отзывов

2. **Сохранение данных в Google-таблицу**:
   - Каждый новый артикул добавляется в новую строку.
   - Если артикул уже существует, данные обновляются.

3. **Экспорт данных**:
   - Команда `/exp` позволяет экспортировать данные Google-таблицы в файл CSV, который отправляется пользователю.

4. **Обработка ошибок**:
   - Если товар не найден, Wildberries или Google API недоступны, бот уведомляет об ошибке.

---

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Akwinchester/wb_parser_bot
   cd wb_parser_bot
   ```

2. Установите зависимости:
   ```bash
   python3 -m venv env
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` в корне проекта и добавьте следующие переменные:
   ```env
   PASSWORD_BOT=<ваш_пароль_для_авторизации>
   BOT_TOKEN=<токен_вашего_Telegram_бота>
   SHEET_ID=<ID_вашей_Google_таблицы>
   SHEET_NAME=<имя_листа_в_таблице>
   ```

4. Настройте учетные данные для Google API:
   - Скачайте JSON-файл учетных данных из [Google Cloud Console](https://console.cloud.google.com/).
   - Переименуйте файл в `service_account.json` и поместите его в папку `wb_parser_bot/credentials/`.

5. Запустите бота:
   ```bash
   python3 main.py
   ```

---

## Пример файла `.env`

```env
PASSWORD_BOT=my_secure_password
BOT_TOKEN=123456789:ABCDEF1234567890abcdef1234567890
SHEET_ID=1aBcD123EfGh456IjKlMnOp789QrSt
SHEET_NAME=Sheet1
```

---

## Файловая структура проекта

```
wb_parser_bot/
├── bot/                            # Логика Telegram-бота
│   ├── __init__.py
│   ├── bot.py                      # Основной файл запуска бота
│   ├── utils.py                    # Утилиты для работы с состояниями и авторизацией
├── google_api/                     # Логика работы с Google API
│   ├── __init__.py
│   ├── google_sheets.py            # Функции работы с Google-таблицами
│   ├── utils.py                    # Утилиты для экспорта данных в CSV
├── parser/                         # Логика парсинга данных Wildberries
│   ├── __init__.py
│   ├── parser.py                   # Основной функционал парсинга
│   ├── requests.py                 # Запросы к API
│   ├── upstreams.py                # Логика выбора хостов Wildberries
│   ├── utils.py                    # Утилиты для обработки данных
├── credentials/                    # Учетные данные для Google API
│   └── service_account.json        # JSON-файл учетных данных (необходимо добавить)
├── data/                           # Папка для сохранения временных файлов (например, CSV)
├── .env                            # Файл с конфиденциальными данными
├── requirements.txt                # Список зависимостей проекта
└── README.md                       # Инструкция по установке и использованию
```

---

## Логирование

- Все ошибки записываются в файл `error.log`.

---

## Поддержка

Если у вас возникли вопросы или проблемы, свяжитесь с разработчиком через GitHub Issues.

