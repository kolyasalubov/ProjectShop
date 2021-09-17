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

    def add_shipping_address(self, user_id: int) -> bool:
        data = self._to_dict()
        response = bot_client.send_request("POST", f"user/{user_id}/shipping-address", data=data)
        return response.status_code == 201

    @staticmethod
    def delete(id):
        response = bot_client.send_request("DELETE", f"/shipping-address?id={id}")
        return response == 200


class Wishlist(Model):
    product_id = IntegerField()
    product_name = StringField(max_value=100)

    def __init__(self, product_id=None,
                 product_name=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.product_id = product_id
        self.product_name = product_name

    def add_wishlist(self, user_id: int) -> bool:
        data = self._to_dict()
        response = bot_client.send_request("POST", f"user/{user_id}/wishlist", data=data)
        return response.status_code == 201

    @staticmethod
    def delete(id):
        response = bot_client.send_request("DELETE", f"/wishlist?id={id}")
        return response == 200


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

    @staticmethod
    def is_registered(phone_number: str) -> object:
        response = bot_client.send_request("GET", f"/user?phone-number={phone_number}")
        if response.status_code == 200:
            return response.json()['id']

    def register(self) -> None:
        response = bot_client.send_request("POST", "/user", data=self._to_dict())
        if response.status_code == 201:
            return response.json()["id"]

    @staticmethod
    def update(user_id: int, data_to_change: dict) -> bool:
        response = bot_client.send_request("PATCH", f"/user?userId={user_id}", data=data_to_change)
        return response.status_code == 200

    @staticmethod
    def get_shipping_addresses(user_id: int) -> list:
        response = bot_client.send_request("GET", f"user/{user_id}/shipping-address")
        if response.status_code == 200:
            return [ShippingAddress._from_dict(s) for s in response.json()]

    @staticmethod
    def get_wishlist(user_id: int) -> list:
        response = bot_client.send_request("GET", f"user/{user_id}/wishlist")
        if response.status_code == 200:
            return [ShippingAddress._from_dict(s) for s in response.json()]


class ProductAttributes(Model):
    name = StringField(max_value=100)

    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name


class Category(ProductAttributes):
    @classmethod
    def get(cls):
        response = bot_client.send_request("GET", "/products/categories")
        if response.status_code == 200:
            return [cls._from_dict(c) for c in response.json()]


class Subcategory(ProductAttributes):
    @classmethod
    def get(cls, category_id):
        response = bot_client.send_request("GET", f"/products/categories/{category_id}/subcategories")
        if response.status_code == 200:
            return [cls._from_dict(s) for s in response.json()]


class Tag(ProductAttributes):
    @classmethod
    def get(cls):
        response = bot_client.send_request("GET", "/products/tags")
        if response.status_code == 200:
            return [cls._from_dict(t) for t in response.json()]


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

    @classmethod
    def view_reviews(cls, product_id):
        response = bot_client.send_request("GET", f"/products/{product_id}/reviews")
        return [cls._from_dict(t) for t in response.json()]

    def post(self, product_id):
        data = self._to_dict()
        response = bot_client.send_request("POST", f"/products/{product_id}/reviews", data=data)
        return response.status_code == 201

    @staticmethod
    def like(self, user_id, review, like=True):
        data = {"userId": user_id, "reply":like}
        response = bot_client.send_request("PUT", f"/products/reviews/{review.id}", data=data)
        if response == 200:
            return response.json()


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

    @staticmethod
    def get(category_id: int, page_size=10, page=1, subcategories=None, tags=None):
        params = {"category": category_id,
                  "bodySize": page_size,
                  "page": page}
        if subcategories:
            params.update({"subcategories": subcategories})
        if tags:
            params.update({"tags": tags})
        response = bot_client.send_request("GET", f"/products", params=params)
        return [Product._from_dict(p) for p in response.json()]


class Order(Model):
    paymentMethod = StringField(max_value=10)
    user_id = IntegerField()
    shipping_address = IntegerField()

    def __init__(self, products,
                 payment_method=None,
                 user_id=None,
                 shipping_address=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.paymentMethod = payment_method
        self.user_id = user_id
        self.shipping_address = shipping_address
        self.products = []

    def add_product(self, product_id, quantity):
        self.products.append({"product":product_id, "quantitu":quantity})

    def submit(self):
        data = self._to_dict()
        response = bot_client.send_request("POST", "/orders", data=data)
        return response == 201
