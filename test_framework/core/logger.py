import os
import time
import logging

from pathlib import Path
from logging.handlers import RotatingFileHandler
from common.settings import LOG_LEVEL, STREAM_LEVEL, FILE_PATH


class LoggerFactory:

    def __init__(self):
        self.log_file = self._init_log_file()

    def _init_log_file(self):
        log_path = FILE_PATH["LOG"]
        if not os.path.exists(log_path): 
            Path(log_path).mkdir(parents=True)
        log_file = os.path.join(log_path, f"test.{time.strftime("%Y%m%d")}.log")
        return log_file

    def get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(LOG_LEVEL)
        
        log_formatter = logging.Formatter(
            "%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s"
        )

        file_handler = RotatingFileHandler(
            filename=self.log_file,
            maxBytes=5_242_880,
            backupCount=3
        )
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(STREAM_LEVEL)
        logger.addHandler(stream_handler)

        return logger
    

factory = LoggerFactory()
logger = factory.get_logger()