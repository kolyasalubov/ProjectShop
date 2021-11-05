from abc import ABC, abstractmethod

from telegram import ReplyMarkup, Message, KeyboardButton
from typing import List, Union


class IMenuBuilder(ABC):
    @abstractmethod
    def create(self) -> Union[ReplyMarkup, List[Message]]:
        pass


class BaseMarkupKeyboardBuilder(IMenuBuilder):
    def __init__(self, data: list, header: list, footer: list, columns):
        self.data = data
        self.header = header
        self.footer = footer
        self.columns = columns

    @abstractmethod
    def _setup_buttons(self) -> None:
        pass


class ReplyMarkupKeyboardBuilder(BaseMarkupKeyboardBuilder):
    def __init__(self, data: List[str], header: List[str], footer: List[str], columns=1, request_location: str = '', request_contact: str = ''):
        super().__init__(data, header, footer, columns)
        self.request_location = request_location
        self.request_contact = request_contact

    def _setup_buttons(self) -> None:
        self.data = [KeyboardButton(text=text, request_contact=(self.request_contact==text), request_location=(self.request_location==text)) for text in self.data]