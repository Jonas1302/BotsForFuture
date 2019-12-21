import logging
from mattermostdriver import Driver

from bff import api
from mmpy_bot.bot import Bot

logger = logging.getLogger(__name__)


class Connection:
    """
    This class allows the user to connect to a Mattermost server and start the bot.
    
    There should be only one instance per program."""
    
    instance = None
    
    def __init__(self, settings):
        assert Connection.instance is None
        self.driver = Driver(settings)
        self.bot = Bot()
        Connection.instance = self
    
    def __getattr__(self, name):
        return getattr(self.driver, name)
    
    
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
