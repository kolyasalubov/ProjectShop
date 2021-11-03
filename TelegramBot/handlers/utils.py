from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Message
from telegram.ext import CallbackContext


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
        return ReplyKeyboardRemove()
