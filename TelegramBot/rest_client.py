import requests

class User:
    def __init__(self, name):
        self.name = name
    @staticmethod
    def deserialize(json):
        return User(json['name'])
    
    def post(self):
        requests.post(self.serialize)

class Order:
    def __init__(self, user):
        self.user = user


user1 = User("Volodya")
order1 = Order(user1)
