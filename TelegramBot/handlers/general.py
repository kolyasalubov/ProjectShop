from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Tuple, List


def create_keyboard(values: List[Tuple[str, str]], columns: int) -> InlineKeyboardMarkup:
    """
    Function to turn list of required for buttons values into actual inline buttons.
    Arguments:
        values: list of pairs button value - button meta. Button meta will be sent back with update
        columns: the number of columns in keyboard
    """
    return InlineKeyboardMarkup([[InlineKeyboardButton(*values[column + row][0])
                                for row in range(columns)]
                                for column in range(0, len(values), columns)])
