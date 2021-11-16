from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Message, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from client.models import Page


def delete_message(context: CallbackContext):
    if isinstance(context.job.context, Message):
        context.job.context.delete()


class KeyboardBuilder:
    def __init__(
        self,
        data: list,
        header: list = None,
        footer: list = None,
        request_location: str = "",
        request_contact: str = "",
    ):
        self.data = [
            KeyboardButton(
                text=button,
                request_location=(request_location is button),
                request_contact=(request_contact is button),
            )
            for button in data
        ]
        self.header = (
            [
                KeyboardButton(
                    text=button,
                    request_location=(request_location is button),
                    request_contact=(request_contact is button),
                )
                for button in header
            ]
            if header
            else None
        )
        self.footer = (
            [
                KeyboardButton(
                    text=button,
                    request_location=(request_location is button),
                    request_contact=(request_contact is button),
                )
                for button in footer
            ]
            if footer
            else None
        )
        self.keyboard = []

    def create(self, columns: int = 1):
        if self.header:
            self.keyboard.append(self.header)
        self.keyboard.extend(
            [self.data[i : i + columns] for i in range(len(self.data) // columns)]
        )
        if self.footer:
            self.keyboard.append(self.footer)
        return ReplyKeyboardMarkup(self.keyboard, resize_keyboard=True)

    @staticmethod
    def remove():
        return ReplyKeyboardRemove(


class InlineKeyboardBuilder:
    """
    This is a builder class for a keyboard
    """

    def __init__(self, page: Page, data: str = None):
        self.page = page
        self.data = data
        self._keyboard = []

    def reset(self):
        self._keyboard = []

    def add_pagination(self) -> None:
        """
        Adds pagination to keyboard if one is required
        """
        if self.page.previous:
            self._keyboard.append(
                [InlineKeyboardButton(text="<", callback_data=self.page.previous)]
            )
            if self.page.next:
                self._keyboard[-1].extend(
                    [InlineKeyboardButton(text=">", callback_data=self.page.next)]
                )
        elif self.page.next:
            self._keyboard.append(
                [InlineKeyboardButton(text=">", callback_data=self.page.next)]
            )

    def create_keyboard(self, text=None, columns=1):
        """
        Method to turn list of required for buttons values into actual inline buttons.
        Arguments:
            text: text to display on buttons, if None - generated dynamically
            columns: the number of columns in keyboard
        """
        self._keyboard = [
            [
                InlineKeyboardButton(
                    text=f"{self.page.results[column + row]}" if not text else text,
                    callback_data=f"{self.data}={self.page.results[column + row].replace(' ', '-')}"
                    if self.data
                    else self.page.results[column + row],
                )
                for row in range(columns)
            ]
            for column in range(0, len(self.page.results), columns)
        ]

        self.add_pagination()

    def add_finish_button(self, data):
        """
        Add button for situations when we need to submit something
        """
        self._keyboard.append(
            [InlineKeyboardButton(text="Finish", callback_data=f"finish-{data}")]
        )

    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(self._keyboard)
        self.reset()
        return keyboard
