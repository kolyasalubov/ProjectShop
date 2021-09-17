from client import bot_client
from model_fields import IntegerField, StringField, DateField, PhoneNumberField, EmailField, DecimalField


class Model:
    """
    Base class for all gathered data. Have methods to initialize objects from dict and serialize objects to dict
    """
    id = IntegerField()

    def __init__(self, id=None, **kwargs):
        self.id = id

    def _to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def _from_dict(cls, _dict: dict) -> object:
        return cls(**_dict)

    def _update(self, data_to_change: dict) -> None:
        self.__dict__.update(data_to_change)


class ShippingAddress(Model):
    postal_code = StringField(max_value=20)
    country = StringField(max_value=50)
    region = StringField(max_value=50)
    city = StringField(max_value=50)
    post_office = IntegerField()

    def __init__(self, postal_code=None,
                 country=None,
                 region=None,
                 city=None,
                 post_office=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.postal_code = postal_code
        self.country = country
        self.region = region
        self.city = city
        self.post_office = post_office


class Wishlist(Model):
    pass


class User(Model):
    first_name = StringField(max_value=40)
    last_name = StringField(max_value=40)
    birth_date = DateField()
    phone_number = PhoneNumberField()
    email = EmailField()

    def __init__(self, first_name=None,
                 last_name=None,
                 birth_date=None,
                 phone_number=None,
                 email=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone_number = phone_number
        self.email = email

    @classmethod
    def is_registered(cls, phone_number: str) -> object:
        response = bot_client.send_request("GET", f"/user?phone-number={phone_number}")
        if response.status_code == 200:
            return cls._from_dict(response.json())

    def register(self) -> None:
        response = bot_client.send_request("POST", "/user", data=self._to_dict())
        if response.status_code == 201:
            self.id = response.json(["id"])

    def update(self, data_to_change: dict) -> None:
        response = bot_client.send_request("PATCH", f"/user?userId={self.id}", data=data_to_change)
        if response.status_code == 200:
            self._update(data_to_change)

    def add_shipping_address(self, shipping_address):
        response = bot_client.send_request("POST", f"user/{self.id}/shipping-address", data=shipping_address)
        return response.status_code == 201

    def get_shipping_addresses(self) -> list:
        response = bot_client.send_request("GET", f"user/{self.id}/shipping-address")
        if response.status_code == 200:
            return [ShippingAddress._from_dict(s) for s in response.json]


class ProductAttributes(Model):
    name = StringField(max_value=100)

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class Category(ProductAttributes):
    pass


class Subcategory(ProductAttributes):
    pass


class Tag(ProductAttributes):
    pass


class Review(Model):
    user_name = StringField(max_value=40)
    rating = IntegerField(max_value=5)
    comment = StringField(max_value=5000)
    likes = IntegerField()
    dislikes = IntegerField()

    def __init__(self, user_name=None,
                 rating=None,
                 comment=None,
                 likes=None,
                 dislikes=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.user_name = user_name
        self.rating = rating
        self.comment = comment
        self.likes = likes
        self.dislikes = dislikes


class Product(Model):
    name = StringField(max_value=100)
    price = DecimalField()
    description = StringField(max_value=5000)
    stock_quantity = IntegerField()

    def __init__(self, name=None,
                 price=None,
                 description=None,
                 stock_quantity=None,
                 categories=None,
                 subcategories=None,
                 tags=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.price = price
        self.description = description
        self.stock_quantity = stock_quantity
        self.categories = [Category._from_dict(c) for c in categories]
        self.subcategories = [Subcategory._from_dict(s) for s in subcategories]
        self.tags = [Tag._from_dict(t) for t in tags]


class Order(Model):
    paymentMethod = StringField(max_value=10)
    user_id = IntegerField()

    def __init__(self, payment_method=None,
                 user_id=None,
                 shipping_address=None,
                 products=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.paymentMethod = payment_method
        self.user_id = user_id
        self.shipping_address = shipping_address
        self.products = products


if __name__ == "__main__":
    x = ShippingAddress()
    x.country = 3
    print(x.country)
