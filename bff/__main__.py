import argparse
import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from bff.api import Connection, MattermostLogHandler
from bff.exceptions import DoNotLoadModuleException
from bff.storage import save_dir
import bff.settings


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
	"""log most exceptions"""
	if issubclass(exc_type, DoNotLoadModuleException):
		logger.info("DoNotLoadModuleException")
	elif issubclass(exc_type, KeyboardInterrupt):
		logger.info("Received KeyboardInterrupt")
		sys.__excepthook__(exc_type, exc_value, exc_traceback)
	else:
		logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = log_exception


# set up cli args parser
parser = argparse.ArgumentParser()
parser.add_argument("--modules", nargs="+", help="only load specific modules")
parser.add_argument("--token", help="use this access token instead of the one specified in settings.json")
args = parser.parse_args()

logger.info(f"run with cli arguments: {args}")

if args.modules:
	bff.settings.settings["modules"] = args.modules
if args.token:
	bff.settings.settings["token"] = args.token
settings = bff.settings.settings


# start bot
logger.info("start bot")
connection = Connection(settings)
connection.login()

if "log-channel" in settings and settings["log-channel"]:
	mattermost_log_handler = MattermostLogHandler(settings["log-channel"])
	mattermost_log_handler.setLevel(logging.ERROR)
	mattermost_log_handler.setFormatter(formatter)
	logging.getLogger().addHandler(mattermost_log_handler)

connection.start()
