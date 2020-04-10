from bff import api


class User:
	def __init__(self, id, username, email, password=None, **kwargs):
		self.id = id
		self.name = username
		self.email = email
		self.password = password
		self.__dict__.update(kwargs)
		self._teams = None
		self._channels = None
	
	def __repr__(self):
		return f"User({self.name})"
	
	def __eq__(self, other):
		if not isinstance(other, User):
			return False
		return self.id == other.id
	
	def __hash__(self):
		return hash(self.id)
	
	@classmethod
	def get_users(cls):
		"""Return a list of all `User`s"""
		return [User(**attrs) for attrs
				in api.users.get_users(params={"page": 0, "per_page": 1<<12})]
	
	@classmethod
	def by_name(cls, name):
		"""Return the user with the given username"""
		if name.startswith("@"):
			name = name[1:]
		return User(**api.users.get_user_by_username(name))
	
	@staticmethod
	def num_users():
		"""Return the total number of users"""
		return api.users.get_stats()
	
	@classmethod
	def by_id(cls, id_):
		"""Return user with the given id"""
		return cls(**api.users.get_user(id_))
	
	@property
	def team(self):
		"""Return the `Team` of the user if theres only one team, else throw an Exception"""
		teams = self.teams
		assert len(teams) == 1, f"{self} must be in exactly one team (currently: {teams})"
		return teams[0]
	
	@property
	def teams(self):
		"""Return a list of all `Team`s of this user"""
		if not self._teams:
			self._teams = [api.Team(**attrs) for attrs in api.teams.get_user_teams(self.id)]
		return self._teams
	
	@property
	def channels(self):
		if not self._channels:
			self._channels = [api.Channel(**attrs) for attrs in api.channels.get_channels_for_user(self.id, self.team.id)]
		return self._channels
	