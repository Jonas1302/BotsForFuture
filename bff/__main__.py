import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from bff.api import Connection
from bff.storage import load, save_dir


log_path = os.path.join(save_dir, "logs", "log.txt")
os.makedirs(os.path.dirname(log_path), exist_ok=True)
file_handler = RotatingFileHandler(log_path, maxBytes=2**22, backupCount=4)
logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%d.%m.%Y %H:%M:%S",
                    level=logging.DEBUG, handlers=[logging.StreamHandler(sys.stdout), file_handler])


logger = logging.getLogger(__name__)

def log_exception(exc_type, exc_value, exc_traceback):
    """Log all exceptions (except `KeyboardInterrupt`)"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = log_exception

logger.info("start bot")
Connection(load("settings.json")).start()
