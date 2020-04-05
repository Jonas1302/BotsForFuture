import logging
from bff import api


logger = logging.getLogger(__name__)


class Channel:
	def __init__(self, id, team_id, name, display_name, type, **kwargs):
		self.id = id
		self.team_id = team_id
		self.name = name
		self.display_name = display_name
		self.type = type
		self.__dict__.update(kwargs)
	
	def __repr__(self):
		return f"Channel({self.id})"
	
	def __eq__(self, other):
		if not isinstance(other, Channel):
			return False
		return self.id == other.id
	
	@classmethod
	def by_id(cls, id_):
		return cls(**api.channels.get_channel(id_))
	
	@classmethod
	def by_team_and_name(cls, team, name):
		return cls(**api.channels.get_channel_by_name(team.id, name))
	
	@classmethod
	def by_name(cls, name):
		logger.warn("using Channel.by_name is discouraged, user Channel.by_team_and_name instead")
		return cls.by_team_and_name(api.me.team, name)
	
	@classmethod
	def by_user(cls, user):
		return cls(**api.channels.create_direct_message_channel([api.me.id, user.id]))
	
	@classmethod
	def by_users(cls, *users):
		return cls(**api.channels.create_group_message_channel([api.me.id, *[user.id for user in users]]))
	
	@property
	def team(self):
		return api.Team.by_id(self.team_id)
	
	def add_user(self, user):
		api.channels.add_user(self.id, options={"user_id": user.id})
	
	@property
	def users(self):
		return [api.User.by_id(attrs["user_id"]) for attrs in
				api.channels.get_channel_members(self.id, params={"page": 0, "per_page": 1<<10})]
