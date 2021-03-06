import logging
from mattermostdriver import Driver
import sys

from bff import api
from bff.settings import convert_to_mmpy_bot
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
		self.bot = Bot(convert_to_mmpy_bot(settings))
		Connection.instance = self
		
		# workaround for python versions < 3.7
		if sys.version_info.major < 3 or sys.version_info.minor < 7:
			api.load_driver_attributes()
	
	def __getattr__(self, name):
		return getattr(self.driver, name)
	
	def login(self):
		logger.info("login...")
		self.driver.login()
		api.me = api.User.by_id(self.driver.client.userid)
		logger.info(f"logged in as {api.me}")
	
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
