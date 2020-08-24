from bff.storage import load

settings = load("settings.json")


def convert_to_mmpy_bot(settings):
	return {
		"BOT_URL": "{scheme}://{url}:{port}{basepath}".format(**settings),
		"BOT_TEAM": settings.get("team"),
		"BOT_LOGIN": settings["login_id"],
		"BOT_PASSWORD": settings["password"],
		"BOT_TOKEN": settings["token"],
		"PLUGINS": ["bff.tasks"],
		"WORKERS_NUM": 1
	}
