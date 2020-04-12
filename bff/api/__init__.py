from .connection import Connection
from .channel import Channel
from .post import Post
from .team import Team
from .user import User
from .utils import MattermostLogHandler, convert_to_post
from mmpy_bot.bot import respond_to, listen_to


def __getattr__(name):
	return getattr(Connection.instance, name)


def load_driver_attributes():
	"""Use this method (when connected to the server) in python versions < 3.7 where __getattr__ won't work"""
	global channels
	global files
	global posts
	global teams
	global users
	
	connection = Connection.instance
	channels = connection.channels
	files = connection.files
	posts = connection.posts
	teams = connection.teams
	users = connection.users
	
