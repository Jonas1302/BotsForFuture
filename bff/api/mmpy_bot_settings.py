"""This module is used as settings module for mmpy_bot"""

from bff.storage import load
from bff.tasks import plugin_paths

settings = load("settings.json")

BOT_URL = "{scheme}://{url}:8065{basepath}".format(**settings)
BOT_TEAM = settings["team"] if "team" in settings else None
BOT_LOGIN = settings["login_id"]
BOT_PASSWORD = settings["password"]
BOT_TOKEN = settings["token"]
PLUGINS = plugin_paths
WORKERS_NUM = 1
