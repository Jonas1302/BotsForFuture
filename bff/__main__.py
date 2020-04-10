import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from bff.storage import load, save_dir


# set up logging
log_path = os.path.join(save_dir, "logs", "log.txt")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

formatter = logging.Formatter("{asctime} {levelname} [{name}] {message}",
							  style="{",
							  datefmt="%d.%m.%Y %H:%M:%S")
file_handler = RotatingFileHandler(log_path, maxBytes=2**20, backupCount=5)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%d.%m.%Y %H:%M:%S",
					level=logging.INFO, handlers=[stream_handler, file_handler])

logger = logging.getLogger(__name__)

def log_exception(exc_type, exc_value, exc_traceback):
	"""Log all exceptions (except `KeyboardInterrupt`)"""
	if issubclass(exc_type, KeyboardInterrupt):
		logger.info("Received KeyboardInterrupt")
		sys.__excepthook__(exc_type, exc_value, exc_traceback)
		return
	logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = log_exception


logger.info("start")
# Set settings for mmpy_bot before importings anything from api!
# We cannot use a settings dict for mmpy_bot directly, instead, we must use a settings module.
# So we add the settings to the global namespace of this module
# and use this module as settings module by setting an environment variable.
# Yes, this is ugly! Maybe we can omit this if we move the mmpy_bot_settings.py file
# to the root of our project?
os.environ["MATTERMOST_BOT_SETTINGS_MODULE"] = "bff.api.mmpy_bot_settings"
sys.path.insert(0, os.path.dirname(__file__))
from bff.api import Connection, MattermostLogHandler, Channel
settings = load("settings.json")
connection = Connection(settings)
connection.login()

if "log-channel" in settings and settings["log-channel"]:
	mattermost_log_handler = MattermostLogHandler(settings["log-channel"])
	mattermost_log_handler.setLevel(logging.INFO)
	mattermost_log_handler.setFormatter(formatter)
	logging.getLogger().addHandler(mattermost_log_handler)

connection.start()
