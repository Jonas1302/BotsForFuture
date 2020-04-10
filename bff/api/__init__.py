from .connection import Connection
from .channel import Channel
from .post import Post
from .team import Team
from .user import User
from .utils import MattermostLogHandler, convert_to_post
from mmpy_bot.bot import respond_to, listen_to


def __getattr__(name):
	return getattr(Connection.instance, name)
