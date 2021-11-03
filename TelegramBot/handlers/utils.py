from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from client.models import Page


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
