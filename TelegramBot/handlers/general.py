from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard(dictionary: dict, columns: int) -> InlineKeyboardMarkup:
    """
    Function to turn list of required for buttons values into actual inline buttons.
    Arguments:
        dictionary: dictionary including our values and next/previous ages urls.
                    Button meta will be sent back with update
        columns: the number of columns in keyboard
    """
    keyboard = [[InlineKeyboardButton(dictionary['results'][column + row][0], dictionary['results'][column + row][0])
                 for row in range(columns)]
                for column in range(0, len(dictionary['results']), columns)]
    if dictionary['previous']:
        keyboard.append(["<", dictionary['previous']])
        if dictionary['next']:
            keyboard[-1].extend([">", dictionary['next']])
    elif dictionary['next']:
        keyboard.append([">", dictionary['next']])
    return InlineKeyboardMarkup(keyboard)
