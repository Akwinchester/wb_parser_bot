from gspread_asyncio import AsyncioGspreadClientManager
from oauth2client.service_account import ServiceAccountCredentials
from config import SERVICE_ACCOUNT_FILE
from my_logging_package import Logger


logger_error = Logger(name="logger_error", log_file='error').get_logger()


def get_creds():
    """Возвращает учетные данные для Google API."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    return ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)

async def get_google_sheet(sheet_id, sheet_name):
    """
    Возвращает объект листа Google Sheets.

    :param sheet_id: ID таблицы.
    :param sheet_name: Название листа.
    :return: Объект листа Google Sheets.
    """
    agcm = AsyncioGspreadClientManager(get_creds)
    agc = await agcm.authorize()  # Авторизация через клиента
    sheet = await agc.open_by_key(sheet_id)
    return await sheet.worksheet(sheet_name)

async def append_or_update_sheet(sheet_id, sheet_name, data, article_index=0):
    """Добавляет данные или обновляет их в Google Sheets."""
    try:
        sheet = await get_google_sheet(sheet_id, sheet_name)
        rows = await sheet.get_all_values()

        for i, row in enumerate(rows):
            if len(row) > article_index and row[article_index] == data[0][article_index]:
                range_label = f"A{i + 1}:{chr(65 + len(data[0]) - 1)}{i + 1}"
                await sheet.update(range_label, [data[0]])
                return True

        await sheet.append_rows(data)
        return True
    except Exception as e:
        logger_error.error(f"Ошибка при обновлении google-таблицы {e}")
        return False

async def export_google_sheet_to_csv(sheet_id, sheet_name, filename=None):
    """Экспортирует данные Google-таблицы в CSV."""
    sheet = await get_google_sheet(sheet_id, sheet_name)
    rows = await sheet.get_all_values()

    if filename is None:
        from datetime import datetime
        filename = f"./data/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"

    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    import csv
    with open(filename, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(rows)

    return filename
