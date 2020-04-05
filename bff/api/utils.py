import logging

from bff import api


logger = logging.getLogger(__name__)


class MattermostLogHandler(logging.Handler):
    """Class which posts log messages to a mattermost channel"""
    
    def __init__(self, channel):
        super().__init__()
        if channel.startswith("~"):
            self.channel = api.Channel.by_name(channel[1:])
        elif channel.startswith("@"):
            raise NotImplementedError
        else:
            raise Exception(f"""unknown log channel {channel}: prefix channel
                            with '~' (or '@' if it's a direct channel to a user)
                            and make sure the bot is in this channel""")
    
    def emit(self, record):
        message = self.format(record)
        api.Post.post(self.channel, message)


def convert_to_post(func):
    def wrapper(message, *args, **kwargs):
        return func(api.Post.by_id(message._body["data"]["post"]["id"]), *args, **kwargs)
    return wrapper
