"""
Models and data validation are implemented using Pydantic BaseModel and fields.
For more info, read https://pydantic-docs.helpmanual.io

Methods in models are facades for all api requests required by telegram bot
"""

import datetime
from enum import Enum
from typing import List, Tuple

from phonenumbers import PhoneNumber
from pydantic import (
    BaseModel,
    constr,
    EmailStr,
    PositiveInt,
    conint,
    condecimal,
    AnyUrl,
)

from client.status_check import bot_client


class Page(BaseModel):
    """
    This model is used to transform gathered data into object
    """

    count: PositiveInt = 1
    next: AnyUrl = None
    previous: AnyUrl = None
    results: list


class PaginatedModel(BaseModel):
    """
    Model for all models, that require pagination
    """

    _path = None
    _name = None

    def __str__(self):
        return getattr(self, self._name)

    @classmethod
    def page(cls, json: dict) -> Page:
        """
        Turn our results into objects of respective class
        """
        json["results"] = [cls(**item) for item in json["results"]]
        return Page(**json)

    @classmethod
    def get(cls) -> Page:
        """
        Get first page of result. Will work only if path provided (in child classes)
        """
        response = bot_client.send_request("GET", cls._path)
        return cls.page(response.json())

    @classmethod
    def turn_page(cls, url: str) -> Page:
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
    def get_shipping_addresses(cls, user_id: int) -> Page:
        """
        Retrieve shipping addresses for user specified by user id

        Return: List[ShippingAddress]
        """
        response = bot_client.send_request(
            "GET", f"user/shipping-address", params={"userId": user_id}
        )
        return cls.page(response.json())

    def add_shipping_address(self):
        """
        Add new shipping address to user addresses list
        """
        bot_client.send_request("POST", f"user/shipping-address", data=self.__dict__)

    @staticmethod
    def delete(address_id: int):
        """
        Delete user's shipping address, specified by user's id and shipping address' id
        """
        bot_client.send_request(
            "DELETE", f"/user/shipping-address", params={"id": address_id}
        )


class Wishlist(PaginatedModel):
    """
    Model for working with users' wishlist. Wishlist's record
    identification is done using product id and user id
    """

    user_id: PositiveInt
    product_id: PositiveInt
    product_name: constr(max_length=100)

    @classmethod
    def get_wishlist(cls, user_id: int) -> Page:
        """
        Retrieve wishlist of certain user specified by user id
        """

        response = bot_client.send_request("GET", f"user/{user_id}/wishlist")
        return cls.page(response.json())

    def add_wishlist(self):
        """
        Add item to user's wishlist
        """
        bot_client.send_request(
            "POST", f"user/{self.user_id}/wishlist", data=self.product_id
        )

    @staticmethod
    def delete(user_id: int, product_id: int):
        """
        Delete item from user's wishlist
        """
        bot_client.send_request(
            "DELETE",
            f"/user/wishlist",
            params={"userId": user_id, "productId": product_id},
        )


class User(BaseModel):
    """
    Model for working with user.
    self.phone_number field uses PhoneNumber class from phonenumbers library,
    everything else - Pydantic fields
    More details on phonenmbers:
    https://github.com/stefanfoulis/django-phonenumber-field
    """

    id: PositiveInt = None
    first_name: constr(max_length=40)
    last_name: constr(max_length=40)
    phone_number: PhoneNumber
    email: EmailStr
    birth_date: datetime.date = None

    class Config:
        """
        Arbitrary_types_allowed allows us to use non-Pydantic classes
        without modification for validation
        """

        arbitrary_types_allowed = True

    @staticmethod
    def is_registered(phone_number: PhoneNumber) -> int:
        """
        Check if our user is registered by his phone_number.
        If he is, return his id for later use
        """
        response = bot_client.send_request(
            "GET", f"/user", params={"phone-number", phone_number}
        )
        return response.json()["id"]

    def register(self) -> int:
        """
        Send user to save in database. On success, return his dedicated id
        """

        response = bot_client.send_request("POST", "/user", data=self.__dict__)
        return response.json()["id"]

    @staticmethod
    def update(user_id: int, data_to_change: dict):
        """
        Change user_data via dict. Return true on success
        """
        bot_client.send_request(
            "PATCH", f"/user", params={"userId", user_id}, data=data_to_change
        )


class Category(PaginatedModel):
    name: constr(max_length=100)

    _path = "/categories"
    _name = "name"


class Tag(PaginatedModel):
    name: constr(max_length=100)

    _path = "/tags"
    _name = "name"


class Review(PaginatedModel):
    """
    Model for reviews. Replies (likes or dislikes) are embedded in model for convenience
    """

    id: PositiveInt
    user_name: constr(max_length=40)
    rating: conint(ge=1, le=5)
    comment: constr(max_length=5000)
    likes: PositiveInt = None
    dislikes: PositiveInt = None

    @classmethod
    def view_reviews(cls, product_id: int) -> Page:
        """
        Here we need to dynamically set our path, so we don`t use base get method
        """

        response = bot_client.send_request("GET", f"/products/{product_id}/reviews")
        return cls.page(response.json())

    def post(self, product_id: int):
        """
        Create new review for product specified by product_id
        """
        bot_client.send_request(
            "POST", f"/products/{product_id}/reviews", data=self.__dict__
        )

    def like(self, user_id, like=True):
        """
        Post a reply for review.
        It`s already posted:
        If reply is the same, supposed to delete it, if another - change it
        """

        data = {"userId": user_id, "reply": like}
        response = bot_client.send_request(
            "PUT", f"/products/reviews/{self.id}/replies", data=data
        )
        return response.json()


class Product(PaginatedModel):
    id = PositiveInt
    name: constr(max_length=100)
    price: condecimal(decimal_places=2, max_digits=9)
    description: constr(max_length=5000)
    stock_quantity: PositiveInt
    categories: List[Category]
    tags: List[Tag]
    images: List[str]
    video_links: List[str]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def view_products(cls, category: str = None, query: list = None) -> Page:
        """
        Get paginated list of products by some filters.
        If filters aren't specified, list should be sorted by popularity
        """
        if category:
            params = {"category": category}
        elif query:
            params = {"query": query}
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

        bot_client.send_request("POST", "/orders", data=self.__dict__)
