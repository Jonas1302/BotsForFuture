from bff import api


class Team:
    def __init__(self, id, **kwargs):
        self.id = id
        self.__dict__.update(kwargs)
        self._channels = None
    
    @classmethod
    def by_id(cls, id_):
        return cls(**api.teams.get_team(id_))
    
    @classmethod
    def by_name(cls, name):
        return cls(**api.teams.get_team_by_name(name))
    
    @property
    def public_channels(self):
        #if not self._channels:
        # update always since new channels may be created
        self._channels = [api.Channel(**attrs) for attrs in
                          api.channels.get_public_channels(self.id, params={"page": 0, "per_page": 1<<10})]
        return self._channels
    
    @property
    def users(self):
        """Return all users in this team"""
        return [api.User.by_id(attrs["user_id"]) for attrs
                in api.teams.get_team_members(self.id, params={"page": 0, "per_page": 1<<10})]
