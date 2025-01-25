import csv
import os
from datetime import datetime
from google_api.google_sheets import get_google_sheet  # Импорт функции для работы с таблицей


def export_google_sheet_to_csv(sheet_id, sheet_name, filename=None):
    """
    Экспортирует данные Google-таблицы в CSV-файл.

    :param sheet_id: ID таблицы Google Sheets.
    :param sheet_name: Название листа в таблице.
    :param filename: Имя файла для экспорта (опционально).
    :return: Путь к созданному файлу.
    """
    # Получение данных из Google-таблицы
    sheet = get_google_sheet(sheet_id, sheet_name)
    data = sheet.get_all_values()  # Получаем все данные из листа

    if filename is None:
        filename = f"./data/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"

    # Проверка существования папки
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Сохранение данных в CSV
    with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')  # Используем ; как разделитель
        writer.writerows(data)

    return filename
