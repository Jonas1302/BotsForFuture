from bff import api


class File:
    def __init__(self, id, **kwargs):
        self.id = id
        self.__dict__.update(kwargs)
    
    @classmethod
    def by_id(cls, id_):
        attrs = api.files.get_file(id_)
        print(attrs)
        return cls(**attrs)
