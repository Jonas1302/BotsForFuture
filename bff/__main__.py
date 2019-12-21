import logging
from logging.handlers import RotatingFileHandler
import os
import sys

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
        logger.info("Received KeyboardInterrupt")
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = log_exception

logger.info("start bot")
# Set settings for mmpy_bot before importings anything from api!
# We cannot use a settings dict for mmpy_bot directly, instead, we must use a settings module.
# So we add the settings to the global namespace of this module
# and use this module as settings module by setting an environment variable.
# Yes, this is ugly! Maybe we can omit this if we move the mmpy_bot_settings.py file
# to the root of our project?
os.environ["MATTERMOST_BOT_SETTINGS_MODULE"] = "bff.api.mmpy_bot_settings"
sys.path.insert(0, os.path.dirname(__file__))
from bff.api import Connection
Connection(load("settings.json")).start()
