from dataclasses import dataclass
from abc import ABC, abstractmethod

from telegram import (
    ReplyMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from typing import List

from utils.Page import IPage

BUTTON_LISTS = ["header", "body", "footer"]


class IMenuBuilder(ABC):
    @property
    @abstractmethod
    def keyboard(self) -> ReplyMarkup:
        pass


@dataclass
class MenuPaginationMixin:
    page: IPage

    def _add_pagination(self, keyboard: List[List[InlineKeyboardButton]], location: int = None) -> None:
        page_turn_buttons = []
        if self.page.previous:
            page_turn_buttons.append(InlineKeyboardButton(text='<', callback_data=self.page.previous))
        if self.page.next:
            page_turn_buttons.append(InlineKeyboardButton(text='>', callback_data=self.page.next))
        if page_turn_buttons:
            if location:
                keyboard.insert(location, page_turn_buttons)
            else:
                keyboard.append(page_turn_buttons)


@dataclass
class BaseMarkupKeyboardBuilder(IMenuBuilder):
    header: list
    body: list
    footer: list
    columns: int

    _button_type: type = ReplyMarkup

    @abstractmethod
    def _setup_buttons(self):
        pass

    def _create_keyboard(self) -> None:
        self._setup_buttons()
        self._keyboard = [
            self.header,
            [
                self.body[i: i + self.columns]
                for i in range(0, len(self.body), self.columns)
            ],
            self.footer,
        ]

    @property
    def keyboard(self) -> ReplyMarkup:
        self._create_keyboard()
        keyboard = self._button_type(self._keyboard)
        return keyboard


@dataclass
class ReplyKeyboardBuilder(BaseMarkupKeyboardBuilder):
    request_location: str = ""
    request_contact: str = ""

    _button_type = ReplyKeyboardMarkup

    def _setup_buttons(self) -> None:
        for button_list in BUTTON_LISTS:
            text_list = getattr(self, button_list)
            setattr(
                self,
                button_list,
                [
                    KeyboardButton(
                        text=text,
                        request_contact=(self.request_contact == text),
                        request_location=(self.request_location == text),
                    )
                    for text in text_list
                ],
            )


@dataclass
class InlineKeyboardBuilder(BaseMarkupKeyboardBuilder):
    name: str = ""

    _button_type = InlineKeyboardMarkup

    def _setup_buttons(self) -> None:
        for button_list in BUTTON_LISTS:
            text_list = getattr(self, button_list)
            setattr(
                self,
                button_list,
                [
                    InlineKeyboardButton(text=text, callback_data=f"{self.name}={text}")
                    for text in text_list
                ],
            )


class PaginatedInlineKeyboardBuilder(InlineKeyboardBuilder, MenuPaginationMixin):

    @property
    def body(self):
        return self.page.body

    def _create_keyboard(self) -> None:
        super()._create_keyboard()
        location = -1 if self.footer else None
        self._add_pagination(keyboard=self._keyboard, location=location)


@dataclass
class MessageMenuBuilder(IMenuBuilder, MenuPaginationMixin):
    body: List[str]
    columns: int = 1

    def _setup_buttons(self, page_part) -> List[InlineKeyboardButton]:
        return [
            InlineKeyboardButton(text=body_part,
                                 callback_data=f"{body_part}={page_part}")
            for body_part in self.body
        ]

    def _structure_one(self, page_part) -> List[List[InlineKeyboardButton]]:
        set_buttons = self._setup_buttons(page_part)
        return [
            set_buttons[i: i + self.columns]
            for i in range(0, len(set_buttons), self.columns)
        ]

    def _create_all(self):
        self._keyboard_list = [self._structure_one(page_part) for page_part in self.page.body]
        self._add_pagination(keyboard=self._keyboard_list[-1])

    @property
    def keyboard(self) -> List[InlineKeyboardMarkup]:
        self._create_all()
        return [InlineKeyboardMarkup(keyboard) for keyboard in self._keyboard_list]
