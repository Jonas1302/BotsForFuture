import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from mmpy_bot.bot import Bot

from bff import Driver


logger = logging.getLogger(__name__)
log_path = "../logs/log.txt"


def log_exception(exc_type, exc_value, exc_traceback):
    """Log all exceptions (except `KeyboardInterrupt`)"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


os.makedirs(os.path.dirname(log_path), exist_ok=True)
file_handler = RotatingFileHandler(log_path, maxBytes=2**22, backupCount=4)
logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%d.%m.%Y %H:%M:%S",
                    level=logging.DEBUG, handlers=[logging.StreamHandler(sys.stdout), file_handler])

sys.excepthook = log_exception
logger.info("start bot")

Driver.create_instance()
Bot().run()
