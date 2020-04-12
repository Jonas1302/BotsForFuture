"""This module is used as settings module for mmpy_bot"""

from bff.settings import settings

BOT_URL = "{scheme}://{url}:{port}{basepath}".format(**settings)
BOT_TEAM = settings["team"] if "team" in settings else None
BOT_LOGIN = settings["login_id"]
BOT_PASSWORD = settings["password"]
BOT_TOKEN = settings["token"]
PLUGINS = ["bff.tasks"]
WORKERS_NUM = 1
