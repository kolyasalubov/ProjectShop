"""
Models and data validation are implemented using Pydantic BaseModel and fields.
For more info, read https://pydantic-docs.helpmanual.io

Methods in models are facades for all api requests required by telegram bot
"""

import datetime
from enum import Enum

from phonenumbers import PhoneNumber
from pydantic import BaseModel, constr, EmailStr, PositiveInt, conint, condecimal
from typing import List, Tuple

from client.status_check import bot_client


class PaginatedModel(BaseModel):
    """
    Model for all models, that require pagination
    """
    _path = None

    @classmethod
    def get(cls):
        """
        Get first page of result. Will work only if path provided (in child classes)
        """
        response = bot_client.send_request("GET", cls._path)
        return cls.page(response.json())

    @classmethod
    def page(cls, json: dict) -> dict:
        """
        Turn our results into objects of respective class
        """
        json['results'] = [cls(**item) for item in json['results']]
        return json

    @classmethod
    def turn_page(cls, url: str) -> dict:
        """
        Change page using given url
        """
        response = bot_client.send_request("GET", url)
        return cls.page(response.json())


class ShippingAddress(PaginatedModel):
    """
    Model to work with shipping addresses.
    """
    id: PositiveInt = None
    user_id: PositiveInt
    postal_code: constr(max_length=20)
    country: constr(max_length=50)
    region: constr(max_length=50)
    city: constr(max_length=50)
    post_office: PositiveInt

    @classmethod
    def get_shipping_addresses(cls, user_id: int) -> dict:
        """
        Retrieve shipping addresses for user specified by user id

        Return: List[ShippingAddress]
        """
        response = bot_client.send_request("GET", f"user/shipping-address", params={"userId": user_id})
        return cls.page(response.json())

    def add_shipping_address(self) -> bool:
        """
        Add new shipping address to user addresses list
        """
        response = bot_client.send_request("POST", f"user/shipping-address", data=self.__dict__)

    @staticmethod
    def delete(address_id: int) -> bool:
        """
        Delete user's shipping address, specified by user's id and shipping address' id
        """
        response = bot_client.send_request("DELETE", f"/user/shipping-address", params={"id": address_id})


class Wishlist(PaginatedModel):
    """
    Model for working with users' wishlist. Wishlist's record identification is done using product id and user id
    """
    user_id: PositiveInt
    product_id: PositiveInt
    product_name: constr(max_length=100)

    @classmethod
    def get_wishlist(cls, user_id: int) -> dict:
        """
        Retrieve wishlist of certain user specified by user id
        """
        response = bot_client.send_request("GET", f"user/{user_id}/wishlist")
        return cls.page(response.json())

    def add_wishlist(self) -> bool:
        """
        Add item to user's wishlist
        """
        response = bot_client.send_request("POST", f"user/{self.user_id}/wishlist", data=self.product_id)

    @staticmethod
    def delete(user_id: int, product_id: int) -> bool:
        """
        Delete item from user's wishlist
        """
        response = bot_client.send_request("DELETE", f"/user/wishlist", params={"userId": user_id,
                                                                                "productId": product_id})


class User(BaseModel):
    """
    Model for working with user.
    self.phone_number field uses PhoneNumber class from phonenumbers library, everything else - Pydantic fields
    More details on phonenmbers: https://github.com/stefanfoulis/django-phonenumber-field
    """
    id: PositiveInt = None
    first_name: constr(max_length=40)
    last_name: constr(max_length=40)
    phone_number: PhoneNumber
    email: EmailStr
    birth_date: datetime.date = None

    class Config:
        """
        Arbitrary_types_allowed allows us to use non-Pydantic classes without modification for validation
        """
        arbitrary_types_allowed = True

    @staticmethod
    def is_registered(phone_number: PhoneNumber) -> int:
        """
        Check if our user is registered by his phone_number. If he is, return his id for later use
        """
        response = bot_client.send_request("GET", f"/user", params={"phone-number", phone_number})
        return response.json()['id']

    def register(self) -> int:
        """
        Send user to save in database. On success, return his dedicated id
        """
        response = bot_client.send_request("POST", "/user", data=self.__dict__)
        return response.json()["id"]

    @staticmethod
    def update(user_id: int, data_to_change: dict) -> bool:
        """
        Change user_data via dict. Return true on success
        """
        response = bot_client.send_request("PATCH", f"/user", params={"userId", user_id}, data=data_to_change)


class Category(PaginatedModel):
    id: PositiveInt
    name: constr(max_length=100)

    _path = "/products/categories"


class Subcategory(BaseModel):
    id: PositiveInt
    name: constr(max_length=100)

    _path = "/products/subcategories"


class Tag(BaseModel):
    id: PositiveInt
    name: constr(max_length=100)

    _path = "/products/tags"


class Review(PaginatedModel):
    """
    Model for reviews. Replies (likes and dislikes) are embedded in model for convenience
    """
    id: PositiveInt
    user_name: constr(max_length=40)
    rating: conint(ge=1, le=5)
    comment: constr(max_length=5000)
    likes: PositiveInt = None
    dislikes: PositiveInt = None

    @classmethod
    def view_reviews(cls, product_id: int) -> dict:
        """
        Here we need to dynamically set our path, so we don`t use base get method
        """
        response = bot_client.send_request("GET", f"/products/{product_id}/reviews")
        return cls.page(response.json())

    def post(self, product_id: int):
        """
        Create new review for product specified by product_id
        """
        response = bot_client.send_request("POST", f"/products/{product_id}/reviews", data=self.__dict__)

    def like(self, user_id, like=True):
        """
        Post a reply for review. If already posted: If reply is the same, supposed to delete it, if another - change it
        """
        data = {"userId": user_id, "reply": like}
        response = bot_client.send_request("PUT", f"/products/reviews/{self.id}/replies", data=data)
        return response.json()


class Product(PaginatedModel):
    id = PositiveInt
    name: constr(max_length=100)
    price: condecimal(decimal_places=2, max_digits=9)
    description: constr(max_length=5000)
    stock_quantity: PositiveInt
    categories: List[Category]
    subcategories: List[Subcategory]
    tags: List[Tag]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def view_products(cls, category_id: int, subcategories: list = None, tags: list = None) -> dict:
        """
        Get paginated list of products by some filters. If filters aren't specified, list should be sorted by popularity
        """
        params = {"category": category_id}
        if subcategories:
            params.update({"subcategories": subcategories})
        if tags:
            params.update({"tags": tags})
        response = bot_client.send_request("GET", f"/products", params=params)
        return cls.page(response.json())


class Order(BaseModel):

    class Payment(str, Enum):
        card = "Card"
        cash = "Cash"

    id: PositiveInt
    paymentMethod: Payment = Payment.cash
    user_id: PositiveInt
    shipping_address: ShippingAddress
    products: List[Tuple[int, int]]

    class Config:
        arbitrary_types_allowed = True

    def add_product(self, product_id, quantity):
        """
        For order in progress, add new product
        """
        self.products.append((product_id, quantity))

    def submit(self):
        """
        Post order to api
        """
        response = bot_client.send_request("POST", "/orders", data=self.__dict__)
