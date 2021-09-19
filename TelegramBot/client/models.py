import datetime
from enum import Enum

from phonenumbers import PhoneNumber
from pydantic import BaseModel, constr, EmailStr, PositiveInt, conint, condecimal
from typing import List, Tuple

from client import bot_client


class ShippingAddress(BaseModel):
    id = PositiveInt
    postal_code: constr(max_length=20)
    country: constr(max_length=50)
    region: constr(max_length=50)
    city: constr(max_length=50)
    post_office: PositiveInt

    @classmethod
    def get_shipping_addresses(cls, user_id: int) -> list:
        response = bot_client.send_request("GET", f"user/{user_id}/shipping-address")
        if response.status_code == 200:
            return [cls(**s) for s in response.json()]

    def add_shipping_address(self, user_id: int) -> bool:
        response = bot_client.send_request("POST", f"user/{user_id}/shipping-address", data=self.__dict__)
        return response.status_code == 201

    @staticmethod
    def delete(id: int):
        response = bot_client.send_request("DELETE", f"/shipping-address", params={"id": id})
        return response == 200


class Wishlist(BaseModel):
    id: PositiveInt
    product_id: PositiveInt
    product_name: constr(max_length=100)

    @classmethod
    def get_wishlist(cls, user_id: int) -> list:
        response = bot_client.send_request("GET", f"user/{user_id}/wishlist")
        if response.status_code == 200:
            return [cls(**w) for w in response.json()]

    def add_wishlist(self, user_id: int) -> bool:
        response = bot_client.send_request("POST", f"user/{user_id}/wishlist", data=self.__dict__)
        return response.status_code == 201

    @staticmethod
    def delete(id: int):
        response = bot_client.send_request("DELETE", f"/wishlist", params={"id": id})
        return response == 200


class User(BaseModel):
    id: PositiveInt = None
    first_name: constr(max_length=40)
    last_name: constr(max_length=40)
    phone_number: PhoneNumber
    email: EmailStr
    birth_date: datetime.date = None

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def is_registered(phone_number: str) -> object:
        response = bot_client.send_request("GET", f"/user?phone-number={phone_number}")
        if response.status_code == 200:
            return response.json()['id']

    def register(self) -> None:
        response = bot_client.send_request("POST", "/user", data=self.__dict__)
        if response.status_code == 201:
            return response.json()["id"]

    @staticmethod
    def update(user_id: int, data_to_change: dict) -> bool:
        response = bot_client.send_request("PATCH", f"/user?userId={user_id}", data=data_to_change)
        return response.status_code == 200


class Category(BaseModel):
    id: PositiveInt
    name: constr(max_length=100)

    @classmethod
    def get(cls):
        response = bot_client.send_request("GET", "/products/categories")
        if response.status_code == 200:
            return [cls(**c) for c in response.json()]


class Subcategory(BaseModel):
    id: PositiveInt
    name: constr(max_length=100)

    @classmethod
    def get(cls, category_id):
        response = bot_client.send_request("GET", f"/products/categories/{category_id}/subcategories")
        if response.status_code == 200:
            return [cls(**s) for s in response.json()]


class Tag(BaseModel):
    id: PositiveInt
    name: constr(max_length=100)

    @classmethod
    def get(cls):
        response = bot_client.send_request("GET", "/products/tags")
        if response.status_code == 200:
            return [cls(**t) for t in response.json()]


class Review(BaseModel):
    id: PositiveInt
    user_name: constr(max_length=40)
    rating: conint(ge=1, le=5)
    comment: constr(max_length=5000)
    likes: PositiveInt
    dislikes: PositiveInt

    @classmethod
    def view_reviews(cls, product_id: int):
        response = bot_client.send_request("GET", f"/products/{product_id}/reviews")
        return [cls(**t) for t in response.json()]

    def post(self, product_id: int):
        response = bot_client.send_request("POST", f"/products/{product_id}/reviews", data=self.__dict__)
        return response.status_code == 201

    def like(self, user_id, like=True):
        data = {"userId": user_id, "reply": like}
        response = bot_client.send_request("PUT", f"/products/reviews/{self.id}", data=data)
        if response == 200:
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
        params = {"category": category_id,
                  "bodySize": page_size,
                  "page": page}
        if subcategories:
            params.update({"subcategories": subcategories})
        if tags:
            params.update({"tags": tags})
        response = bot_client.send_request("GET", f"/products", params=params)
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
        self.products.append((product_id, quantity))

    def submit(self):
        response = bot_client.send_request("POST", "/orders", data=self.__dict__)
        return response == 201
