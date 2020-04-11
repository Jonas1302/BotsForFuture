import logging
from bff.api import User, Team, Channel, respond_to, convert_to_post
from bff.settings import settings
from bff.exceptions import DoNotLoadModuleException
from .utils import targets_to_users

logger = logging.getLogger(__name__)


# check if this module shall be loaded
if settings["modules"] and __name__ not in settings["modules"]:
	logger.info(f"{__name__} shall not be loaded")
	raise DoNotLoadModuleException(__name__)


mail_pattern = "{name} &lt;{email}&gt;"  # '<' and '>' would not be displayed by Mattermost Markdown
mail_separator = ", "


@respond_to("^(?i)mails$")
@respond_to("^(?i)mails (.*)$")
@convert_to_post
def post_mails(post, target_list=None):
	users = targets_to_users(post, target_list)
	logger.debug(f"post mails for users: {users}")
	addresses = []
	
	for user in users:
		addresses.append(mail_pattern.format(name=user.name, email=user.email))
	
	text = mail_separator.join(addresses)
	post.reply(text)
	return text
