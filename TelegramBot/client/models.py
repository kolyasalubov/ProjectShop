"""
Models and data validation are implemented using Pydantic BaseModel and fields.
For more info, read https://pydantic-docs.helpmanual.io

Methods in models are facades for all api requests required by telegram bot
"""

import datetime
from enum import Enum
from typing import List, Tuple

from phonenumbers import PhoneNumber
from pydantic import BaseModel, constr, EmailStr, PositiveInt, conint, condecimal

from client.client import bot_client


class ShippingAddress(BaseModel):
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
    def get_shipping_addresses(cls, user_id: int) -> list:
        """
        Retrieve shipping addresses for user specified by user id

        Return: List[ShippingAddress]
        """

        response = bot_client.send_request(
            "GET", "user/shipping-address", params={"userId": user_id}
        )
        if response.status_code == 200:
            return [cls(**s) for s in response.json()]

    def add_shipping_address(self) -> bool:
        """
        Add new shipping address to user addresses list
        """

        response = bot_client.send_request(
            "POST", "user/shipping-address", data=self.__dict__
        )
        return response.status_code == 201

    @staticmethod
    def delete(address_id: int) -> bool:
        """
        Delete user's shipping address, specified by user's id and shipping address' id
        """

        response = bot_client.send_request(
            "DELETE", "/user/shipping-address", params={"id": address_id}
        )
        return response.status_code == 200


class Wishlist(BaseModel):
    """
    Model for working with users' wishlist. Wishlist's record identification is done using product id and user id
    """

    user_id: PositiveInt
    product_id: PositiveInt
    product_name: constr(max_length=100)

    @classmethod
    def get_wishlist(cls, user_id: int) -> list:
        """
        Retrieve wishlist of certain user specified by user id
        """

        response = bot_client.send_request("GET", f"user/{user_id}/wishlist")
        if response.status_code == 200:
            return [cls(**w) for w in response.json()]

    def add_wishlist(self) -> bool:
        """
        Add item to user's wishlist
        """

        response = bot_client.send_request(
            "POST", f"user/{self.user_id}/wishlist", data=self.product_id
        )
        return response.status_code == 201

    @staticmethod
    def delete(user_id: int, product_id: int) -> bool:
        """
        Delete item from user's wishlist
        """

        response = bot_client.send_request(
            "DELETE",
            "/user/wishlist",
            params={"userId": user_id, "productId": product_id},
        )
        return response.status_code == 200


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

        response = bot_client.send_request(
            "GET", "/user", params={"phone-number", phone_number}
        )
        if response.status_code == 200:
            return response.json()["id"]

    def register(self) -> int:
        """
        Send user to save in database. On success, return his dedicated id
        """

        response = bot_client.send_request("POST", "/user", data=self.__dict__)
        if response.status_code == 201:
            return response.json()["id"]

    @staticmethod
    def update(user_id: int, data_to_change: dict) -> bool:
        """
        Change user_data via dict. Return true on success
        """

        response = bot_client.send_request(
            "PATCH", "/user", params={"userId", user_id}, data=data_to_change
        )
        return response.status_code == 200


class Category(BaseModel):
    id: PositiveInt
    name: constr(max_length=100)

    @classmethod
    def get(cls) -> list:
        """Get category list"""

        response = bot_client.send_request("GET", "/products/categories")
        if response.status_code == 200:
            return [cls(**c) for c in response.json()]


class Subcategory(BaseModel):
    id: PositiveInt
    name: constr(max_length=100)

    @classmethod
    def get(cls, category_id: int) -> list:
        """
        Get subcategory list by category
        """

        response = bot_client.send_request("GET", "/products/subcategories")
        if response.status_code == 200:
            return [cls(**s) for s in response.json()]


class Tag(BaseModel):
    id: PositiveInt
    name: constr(max_length=100)

    @classmethod
    def get(cls) -> list:
        """
        Get tags list
        """

        response = bot_client.send_request("GET", "/products/tags")
        if response.status_code == 200:
            return [cls(**t) for t in response.json()]


class Review(BaseModel):
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
    def view_reviews(cls, product_id: int) -> list:
        """
        Get list of reviews for specified product
        """

        response = bot_client.send_request("GET", f"/products/{product_id}/reviews")
        return [cls(**t) for t in response.json()]

    def post(self, product_id: int):
        """
        Create new review for product specified by product_id
        """

        response = bot_client.send_request(
            "POST", f"/products/{product_id}/reviews", data=self.__dict__
        )
        return response.status_code == 201

    def like(self, user_id, like=True):
        """
        Post a reply for review. If already posted: If reply is the same, supposed to delete it, if another - change it
        """

        data = {"userId": user_id, "reply": like}
        response = bot_client.send_request(
            "PUT", f"/products/reviews/{self.id}/replies", data=data
        )
        if response.status_code == 200:
            return response.json()


class Product(BaseModel):
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
    def get(cls, category_id: int, page_size=10, page=1, subcategories=None, tags=None):
        """
        Get paginated list of products by some filters. If filters aren't specified, list should be sorted by popularity
        """

        params = {"category": category_id, "bodySize": page_size, "page": page}
        if subcategories:
            params.update({"subcategories": subcategories})
        if tags:
            params.update({"tags": tags})
        response = bot_client.send_request("GET", "/products", params=params)
        return [cls(**p) for p in response.json()]


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
        return response.status_code == 201
