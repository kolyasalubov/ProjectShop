from client import bot_client


class Model:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def from_json(self, json):
        self.__init__(**json)
