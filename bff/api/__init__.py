from mmpy_bot.bot import respond_to, listen_to

from .connection import Connection
from .channel import Channel
from .post import Post
from .team import Team
from .user import User


def __getattr__(name):
    return getattr(Connection.instance, name)
