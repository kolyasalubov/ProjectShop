class NameFieldError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"This name field is already occupied: {self.name}"
