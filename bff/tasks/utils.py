import logging
from bff.api import User, Channel, Team

logger = logging.getLogger(__name__)

def targets_to_users(post, target_list):
	# targets may be users (with or without '@'), channels with '~' or teams
	
	if not target_list:
		logger.info([u.__dict__ for u in User.get_users()])
		return User.get_users()
	
	targets = list(map(str.strip, target_list.split()))
	users = set()
	
	for target in targets:
		if target in ("all", "channel", "@all", "@channel"):
			# Note: this method is actually not called for '@all' and '@channel'
			# add all users in the current channel
			users.update(post.channel.users)
		elif target.startswith("~"):
			# add all users in the specific channel
			users.update(Channel.by_team_and_name(post.channel.team, target).users)
		else:
			try:
				# try to find a user with the given name
				users.add(User.by_name(target))
			except Exception:
				# it's not a user therefore we assume it's a team name
				users.update(Team.by_name(target).users)
	return users
