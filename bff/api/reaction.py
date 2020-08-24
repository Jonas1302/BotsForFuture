import logging
from bff import api

logger = logging.getLogger(__name__)


class Reaction:
	def __init__(self, user_id, post_id, emoji_name, **kwargs):
		self.user_id = user_id
		self.post_id = post_id
		self.emoji = emoji_name
		self.__dict__.update(kwargs)
		self._user = None
		self._post = None
	
	def __eq__(self, other):
		if not isinstance(other, Reaction):
			return False
		return self.user == other.user \
			and self.post == other.post \
			and self.emoji == other.emoji
	
	def __hash__(self):
		return hash(self.user, self.post, self.emoji)
	
	@property
	def user(self):
		if not self._user:
			self._user = api.User.by_id(self.user_id)
		return self._user
	
	@property
	def post(self):
		if not self._post:
			self._post = api.Post.by_id(self.post_id)
		return self._post
