"""
Models and data validation are implemented using Pydantic BaseModel and fields.
For more info, read https://pydantic-docs.helpmanual.io

Methods in models are facades for all api requests required by telegram bot
"""

import os
import datetime
import phonenumbers
from enum import Enum

from pydantic import BaseModel, constr, EmailStr, PositiveInt, conint, condecimal, validator
from pydantic.error_wrappers import ValidationError
from typing import List, Tuple

from client.status_check import bot_client

USER_URL = "api/v1/user/"  # add url to obtain and manage user by phone number
USER_INIT_KEY = os.environ.get("USER_INIT_KEY")   # key for User.__init__  access, set None to switch off
USER_BY_TELEGRAM_ID_URL = "api/v1/get_user_by_telegram_id/"  # add url to obtain user by telegram id


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
    Model for working with users' wishlist. Wishlist's record
    identification is done using product id and user id
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
    Pydantic model class for working with user model and relative djangoREST database user model.
    """
    id: PositiveInt
    telegram_id: constr(max_length=40)
    first_name: constr(max_length=40)
    last_name: constr(max_length=40)
    phone_number: constr(max_length=20)
    email: EmailStr
    birth_date: datetime.date = None

    @staticmethod
    def _get_restricted_fields():
        """
        Return names of fields restricted to change.
        :return: tuple
        """
        return "id", "telegram_id", "phone_number", "email"

    @classmethod
    def _validate_fields(cls, **kwargs):
        """
        Validate value for field. Raise ValidationError
        :param kwargs: dict
        :return: None
        """
        cls(
            key=USER_INIT_KEY,
            id=1,
            telegram_id=kwargs.get("telegram_id", ""),
            first_name=kwargs.get("first_name", ""),
            last_name=kwargs.get("last_name", ""),
            phone_number=kwargs.get("phone_number", "+380666666666"),
            email=kwargs.get("email", "email@email.com"),
            birth_date=kwargs.get("birth_date", None),
        )

    def __init__(self, key=None, **kwargs):
        """
        Initialize User instance. Allow initializing only if <key> parameter match with USER_INIT_KEY constant.
        Raise PermissionError if else.
        :param key: any type
        :param kwargs: dict
        """
        if key == USER_INIT_KEY:
            super().__init__(**kwargs)
        else:
            raise PermissionError("Direct creation is restricted. Use class methods.")

    class Config:
        """
        Arbitrary_types_allowed allows us to use non-Pydantic classes
        without modification for validation
        """

        arbitrary_types_allowed = True

    def __setattr__(self, key, value):
        """
        Set user attribute only after changing in relative djangoREST database user model.
        Restrict changing restricted fields.
        """
        if key in self._get_restricted_fields():
            raise PermissionError(f"{key} is not changeable field")
        data = {key: value}
        User._validate_fields(**data)
        url = USER_URL + self.phone_number + "/"
        data = {key: value}
        bot_client.send_request("PATCH", url, data=data)
        super().__setattr__(key, value)

    @validator("phone_number")
    def phone_number_must_be_valid(cls, value):
        """
        Validate phone number field. Raise ValidationError if not valid.
        :param value: str
        :return: None
        """
        try:
            phone_number = phonenumbers.parse(value)
            if phonenumbers.is_valid_number(phone_number):
                return value
            raise ValidationError
        except Exception:
            raise ValidationError

    @classmethod
    def _create_user(cls, user_response):
        """
        Create User instance from response body data.
        :param user_response: requests.Response
        :return: User instance
        """
        user = user_response.json()
        user = cls(
            key=USER_INIT_KEY,
            id=user.get("id"),
            telegram_id=user.get("telegram_id"),
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            phone_number=user.get("phone_number"),
            email=user.get("email"),
            birth_date=user.get("birth_date"),
        )
        return user

    @classmethod
    def register_user(cls, telegram_id, phone_number, email, first_name, last_name, birth_date=None):
        """
        Register user in djangoREST database and crete appropriate User instance.
        :param telegram_id: str
        :param phone_number: str
        :param email: str
        :param first_name: str
        :param last_name: str
        :param birth_date: str
        :return: User instance
        """
        user_data = {
            "telegram_id": telegram_id,
            "phone_number": phone_number,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date
        }
        User._validate_fields(**user_data)
        user_response = bot_client.send_request("POST", USER_URL, data=user_data)
        return cls._create_user(user_response)

    @staticmethod
    def _patch_user_telegram_id(phone_number, telegram_id):
        """
        Add telegram id to user model in djangoREST database.
        :param phone_number: str
        :param telegram_id: str
        :return: requests.Response
        """
        url = USER_URL + phone_number + "/"
        data = {"telegram_id": telegram_id}
        User._validate_fields(**data)
        response = bot_client.send_request("PATCH", url, data=data)
        return response

    @classmethod
    def get_user_by_telegram_id(cls, telegram_id):
        """
        Get user from djangoREST database by telegram id.
        Create and return appropriate User instance.
        :param telegram_id: str
        :return: User instance
        """
        url = USER_BY_TELEGRAM_ID_URL + telegram_id + "/"
        user_response = bot_client.send_request("GET", url)
        return cls._create_user(user_response)

    @classmethod
    def get_user_by_phone_number(cls, phone_number, telegram_id):
        """
        Get user from djangoREST database by phone number.
        Create and return appropriate User instance.
        :param phone_number: str
        :param telegram_id: str
        :return: User instance
        """
        User._validate_fields(telegram_id=telegram_id)
        user_response = cls._patch_user_telegram_id(phone_number, telegram_id)
        return cls._create_user(user_response)


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
    Model for reviews. Replies (likes or dislikes) are embedded in model for convenience
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
        Post a reply for review.
        It`s already posted:
        If reply is the same, supposed to delete it, if another - change it
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
        Get paginated list of products by some filters.
        If filters aren't specified, list should be sorted by popularity
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
