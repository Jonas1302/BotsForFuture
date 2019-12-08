import logging
from mattermostdriver import Driver
import os
import sys

from bff import api
from . import mmpy_bot_settings

logger = logging.getLogger(__name__)


class Connection:
    instance = None
    
    def __init__(self, settings):
        assert Connection.instance is None
        self.driver = Driver(settings)
        self._load_bot(settings)
        Connection.instance = self
    
    def __getattr__(self, name):
        return getattr(self.driver, name)
    
    def _load_bot(self, settings):
        # We cannot use a settings dict for mmpy_bot directly,
        # instead, we must use a settings module.
        # So we add the settings to the global namespace of this module
        # and use this module as settings module by setting an environment variable.
        # Yes, this is ugly!
        os.environ["MATTERMOST_BOT_SETTINGS_MODULE"] = "mmpy_bot_settings"
        sys.path.insert(0, os.path.dirname(__file__))
        
        # now we can load our bot
        from mmpy_bot.bot import Bot
        self.bot = Bot()
    
    def start(self):
        logger.info("Conenction.start")
        self.driver.login()
        logger.info("logged in with mattermostdriver")
        self.me = api.User.by_id(self.driver.client.userid)
        logger.info(f"logged in as {self.me}")
        
        # start bot at the end because the method will not return unless an exception occurs
        self.bot.run()
    
    def stop(self):
        self.driver.logout()
        # TODO stop bot
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, type, value, tb):
        self.stop()
    

class MattermostLogHandler(logging.Handler):
    def __init__(self, channel):
        self.channel = channel
    
    def emit(self, record):
        message = self.format(record)
        api.Post.post(self.channel, message)
