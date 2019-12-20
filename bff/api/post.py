from bff import api

class Post:
    def __init__(self, id, channel_id, message, **kwargs):
        self.id = id
        self.channel_id = channel_id
        self.message = message
        self.__dict__.update(kwargs)
        self._channel = None
        self._thread = None
        self._root = None
        self._files = None
    
    @classmethod
    def post(cls, channel, message, root_post=None, files=[]):
        assert len(files) <= 5, "only 5 files are allowed per post"
        options={"channel_id": channel.id, 
                 "message": message,
                 "root_id": root_post.id,
                 "file_ids": [f.id for f in files],
                 "props": None}
        return cls(**api.posts.create_post(options))
    
    @classmethod
    def ephemeral_post(cls, user, channel, message):
        options={"user_id": user.id,
                 "post": {"channel_id": channel.id, 
                          "message": message}}
        return cls(**api.posts.create_post(options))
    
    @classmethod
    def by_id(cls, id_):
        return cls(**api.posts.get_post(id_))
    
    @property
    def channel(self):
        if not self._channel:
            self._channel = api.Channel.by_id(self.channel_id)
        return self._channel
    
    @property
    def thread(self):
        if not self._thread:
            t = api.posts.get_thread(self.id)
            # Note: we should sort the posts manually
            posts = {post["id"]: Post(**post) for post in t["posts"]}
            self._thread = Thread([posts[id_] for id_ in t["order"]])
        return self._thread
    
    @property
    def root(self):
        if not self._root:
            self._root = Post.by_id(self.root_id)
        return self._root
    
    @property
    def files(self):
        if not self._files:
            self._files = [api.File(**attrs) for attrs in api.posts.get_file_info_for_post(self.id)]
        return self._files


class Thread:
    def __init__(self, posts):
        self.posts = posts
    
    def __len__(self):
        return len(self.posts)