import logging

import mattermostdriver
from mmpy_bot import settings


logger = logging.getLogger(__name__)


def get_config():
    return {"url": settings.SERVER_URL,
            "scheme": settings.SERVER_SCHEME,
            "port": settings.SERVER_PORT,
            "login_id": settings.BOT_LOGIN,
            "password": settings.BOT_PASSWORD,
            "token": settings.BOT_TOKEN}


class Driver(mattermostdriver.Driver):
    instance = None
    
    def __init__(self):
        super().__init__(get_config())
        self.login()
        logger.info(f"Logged in as {self.client.username}")
    
    
    @staticmethod
    def create_instance():
        if Driver.instance:
            raise Exception("Driver instance already exists")
        Driver.instance = Driver()
