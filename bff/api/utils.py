import logging

from bff import api


logger = logging.getLogger(__name__)


class MattermostLogHandler(logging.Handler):
	"""Class which posts log messages to a mattermost channel"""
	
	def __init__(self, channel):
		super().__init__()
		if channel.startswith("@"):
			self.channel = api.Channel.by_user(api.User.by_name(channel))
		else:
			self.channel = api.Channel.by_name(channel)
	
	def emit(self, record):
		message = self.format(record)
		api.Post.post(self.channel, message)


def convert_to_post(func):
	def wrapper(message, *args, **kwargs):
		return func(api.Post.by_id(message._body["data"]["post"]["id"]), *args, **kwargs)
	return wrapper
