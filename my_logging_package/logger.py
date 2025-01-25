import logging
from .config import create_file_handler

class Logger:
    def __init__(self, name, log_file='main_log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        file_handler = create_file_handler(log_file)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger