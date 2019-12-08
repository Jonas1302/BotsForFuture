from bff import api


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
    
    @classmethod
    def by_id(cls, id_):
        return [cls(**api.channels.get_channel(id_))]
    
    @classmethod
    def by_team_and_name(cls, team, name):
        return cls(**api.channels.get_channel_by_name(team.id, name))
    
    @classmethod
    def by_name(cls, name):
        return cls.by_team_and_name(api.me.team, name)
    
    @property
    def team(self):
        return api.Team.by_id(self.team_id)
    
    def add_user(self, user):
        api.channels.add_user(self.id, options={"user_id": user.id})
    
    @property
    def users(self):
        return [api.User(**attrs) for attrs in
                api.channels.get_channel_members_for_user(api.me.id, api.me.team.id)]
