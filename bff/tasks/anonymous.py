import logging
import re

from bff.api import User, Channel, Post, listen_to, respond_to, convert_to_post, me
from bff import storage

logger = logging.getLogger(__name__)


regex = "\\A(@\\S+)" + "( @\\S+)?" * 6 + ".+\\Z"

undefined_default_target_message = \
	"Scheinbar stimmt hier was mit den Einstellungen nicht!\n" \
	"Wende dich an @jonas oder schreibe an den Anfang deiner Nachricht explizit, " \
	"an wen diese gesendet werden soll (mittels @ am Anfang des Namens)"


data = storage.get_storage("anonymous")

# initialize data
was_uninitialized = False
if data.root_posts is None:
	data.root_posts = {}
	was_uninitialized = True
if data.default_target is None:
	data.default_target = ""
	was_uninitialized = True

if was_uninitialized:
	logger.warn("module storage was not completly initialized")
	data.save()


def is_targeted(post):
	# we are tagged at the beginning of the message but there should be also another user be tagged
	#if post.message.startswith(f"@{me.name} "):
	#	return True
	# the post is a response to a post from us
	if post.root and post.root.user == me:
		return True
	# it's a direct channel with us
	if post.channel == Channel.by_user(post.user):
		return True
	return False


# Note: First @user is ignored in direct channel when matching respond_to regex
@listen_to(".*")
@respond_to(".*")
@convert_to_post
def send_anonymously(post):
	# we listen to all messages, thus check if we shall even get notified
	# do not use "respond_to" since it will not process responses in group channels
	if not is_targeted(post):
		return
	
	# differ between first post (without a root) and responses
	if not post.root:
		# calc user names
		match = re.match(regex, post.message, re.MULTILINE + re.DOTALL)
		if match is None:
			names = data.default_target.split(",")
			# default_target may also be an empty string thus the latter check
			if len(names) == 0 or sum(map(len, names)) == 0:
				post.reply(undefined_default_target_message)
				return
		else:
			names = filter(None, match.groups())
		users = [User.by_name(name.strip()) for name in names]
		
		anonymous_post = Post.post(users, post.message)
		
		# store information for responses
		data.root_posts[post.id] = {
			"other_post": anonymous_post.id,
			"other_channel": anonymous_post.channel_id}
		data.root_posts[anonymous_post.id] = {
			"other_post": post.id,
			"other_channel": post.channel_id}
		data.save()
		
		post.reply(f"Nachricht an {', '.join(['@' + u.name for u in users])} gesendet. Das nachträgliche Bearbeiten der Nachricht ist leider noch nicht möglich.")
	else:
		bridge_info = data.root_posts[post.root.id]
		root_post = Post.by_id(bridge_info["other_post"])
		channel = Channel.by_id(bridge_info["other_channel"])
		Post.post(channel, post.message, root_post)
		post.reply("Antwort gesendet. Das nachträgliche Bearbeiten der Nachricht ist leider noch nicht möglich.")



# old implementation
"""
username = me.name
assert username.startswith("awareness-")
target_user = User.by_name(username[len("awareness-"):])

# Note: First @user is ignored in direct channel
@respond_to("^.*$")
@convert_to_post
def send_anonymously(post, *targets):
	Post.post(target_user, post.message)
"""

