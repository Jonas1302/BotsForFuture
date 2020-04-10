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
		#self.driver.client.activate_verbose_logging()
		self.bot = Bot()
		Connection.instance = self
	
	def __getattr__(self, name):
		return getattr(self.driver, name)
	
	def login(self):
		logger.info("login...")
		self.driver.login()
		self.me = api.User.by_id(self.driver.client.userid)
		logger.info(f"logged in as {self.me}")
	
	def start(self):
		# start bot at the end because the method will not return unless an exception occurs
		logger.info("start bot...")
		self.bot.run()
		logger.info("bot started")
	
	def stop(self):
		self.driver.logout()
		# TODO stop bot
	
	def __enter__(self):
		self.start()
		return self
	
	def __exit__(self, type, value, tb):
		self.stop()
