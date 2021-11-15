from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

from client.client import RestClient, bot_client


BUTTON_REGISTER = "Register"
BUTTON_SHOW_PRODUCTS = "Go to products"
BUTTON_SHOW_MY_ORDERS = "Show my orders"
BUTTON_PROFILE = "My profile"


def get_base_reply_keyboard():
    """
    Register keyboard buttons into the menu
    """
    keyboard = [
        [
            KeyboardButton(BUTTON_REGISTER),
            KeyboardButton(BUTTON_SHOW_PRODUCTS),
            KeyboardButton(BUTTON_SHOW_MY_ORDERS),
            KeyboardButton(BUTTON_PROFILE),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
