from .connection import Connection
from .channel import Channel
from .post import Post
from .reaction import Reaction
from .team import Team
from .user import User
from .utils import MattermostLogHandler, convert_to_post, convert_to_reaction
from mmpy_bot.bot import respond_to, listen_to, post_edited, post_deleted, reaction_added, reaction_removed, at_start


# used by the modules in this package to access the old API
def __getattr__(name):
	return getattr(Connection.instance, name)


def load_driver_attributes():
	"""Use this method (when connected to the server) in python versions < 3.7 where __getattr__ won't work"""
	global channels
	global files
	global posts
	global teams
	global users
	global me
	
	connection = Connection.instance
	channels = connection.channels
	files = connection.files
	posts = connection.posts
	teams = connection.teams
	users = connection.users
	me = None  # is set later in Connection after logging in
	
