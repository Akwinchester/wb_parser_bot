import logging
import os
from datetime import datetime
import pytz
from multiprocessing import current_process

# Класс форматтера для добавления часового пояса в логи
class TimezoneFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, tz=None):
        super().__init__(fmt, datefmt)
        self.tz = pytz.timezone(tz) if tz else pytz.utc

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=pytz.utc)
        local_dt = dt.astimezone(self.tz)
        return local_dt.strftime(datefmt) if datefmt else local_dt.isoformat()

# Функция для создания уникального обработчика для логгера
def create_file_handler(log_file):
    """
    Создает и возвращает обработчик для записи в указанный файл.
    """
    log_path = os.getenv('LOG_PATH', f'logs/{log_file}.log')
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = TimezoneFormatter(
        fmt='%(asctime)s [%(levelname)s](%(name)s): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        tz='Europe/Moscow'
    )

    handler = logging.FileHandler(log_path, encoding='utf-8')
    handler.setFormatter(formatter)
    return handler