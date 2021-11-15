from dataclasses import dataclass
from abc import abstractmethod

from telegram import (
    ReplyMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from typing import List

from interfaces.callback_items import IMenuBuilder
from interfaces.models import IPage

BUTTON_LISTS = ["header", "body", "footer"]


@dataclass
class MenuPaginationMixin:
    page: IPage

    def _add_pagination(
        self, keyboard: List[List[InlineKeyboardButton]], location: int = None
    ) -> None:
        page_turn_buttons = []
        if self.page.previous:
            page_turn_buttons.append(
                InlineKeyboardButton(
                    text="<", callback_data=f"url={self.page.previous}"
                )
            )
        if self.page.next:
            page_turn_buttons.append(
                InlineKeyboardButton(text=">", callback_data=f"url={self.page.next}")
            )
        if page_turn_buttons:
            if location:
                keyboard.insert(location, page_turn_buttons)
            else:
                keyboard.append(page_turn_buttons)


@dataclass
class BaseMarkupKeyboardBuilder(IMenuBuilder):

    body: list = None
    header: list = None
    footer: list = None
    columns: int = 1

    @property
    @abstractmethod
    def button_type(self) -> type(ReplyMarkup):
        pass

    @button_type.setter
    @abstractmethod
    def button_type(self, type_: type(ReplyMarkup)):
        pass

    @abstractmethod
    def _setup_buttons(self):
        pass

    def _create_keyboard(self) -> None:
        self._setup_buttons()
        if self.header:
            self._keyboard = [self.header]
        else:
            self._keyboard = []
        self._keyboard.extend(
            [
                self.body[i : i + self.columns]
                for i in range(0, len(self.body), self.columns)
            ],
        )
        if self.footer:
            self._keyboard.append(self.footer)

    @property
    def keyboard(self) -> ReplyMarkup:
        self._create_keyboard()
        keyboard = self.button_type(self._keyboard)
        return keyboard


@dataclass
class ReplyKeyboardBuilder(BaseMarkupKeyboardBuilder):
    request_location: str = ""
    request_contact: str = ""

    button_type = ReplyKeyboardMarkup

    def _setup_buttons(self) -> None:
        for button_list in BUTTON_LISTS:
            text_list = getattr(self, button_list)
            if text_list:
                setattr(
                    self,
                    button_list,
                    [
                        KeyboardButton(
                            text=str(text),
                            request_contact=(self.request_contact == text),
                            request_location=(self.request_location == text),
                        )
                        for text in text_list
                    ],
                )


class RemoveReplyKeyboard(IMenuBuilder):
    @property
    def keyboard(self) -> ReplyMarkup:
        return ReplyKeyboardRemove()


@dataclass
class InlineKeyboardBuilder(BaseMarkupKeyboardBuilder):
    name: str = ""

    button_type = InlineKeyboardMarkup

    def _setup_buttons(self) -> None:
        for button_list in BUTTON_LISTS:
            text_list = getattr(self, button_list)
            if text_list:
                setattr(
                    self,
                    button_list,
                    [
                        InlineKeyboardButton(
                            text=str(text), callback_data=f"{self.name}={text}"
                        )
                        for text in text_list
                    ],
                )


@dataclass
class PaginatedInlineKeyboardBuilder(InlineKeyboardBuilder, MenuPaginationMixin):

    button_type = InlineKeyboardMarkup

    @property
    def body(self):
        return self.page.body

    @body.setter
    def body(self, body):
        if body:
            self.page.body = body

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
            InlineKeyboardButton(
                text=str(body_part), callback_data=f"{body_part}={page_part}"
            )
            for body_part in self.body
        ]

    def _structure_one(self, page_part) -> List[List[InlineKeyboardButton]]:
        set_buttons = self._setup_buttons(page_part)
        return [
            set_buttons[i : i + self.columns]
            for i in range(0, len(set_buttons), self.columns)
        ]

    def _create_all(self):
        self._keyboard_list = [
            self._structure_one(page_part) for page_part in self.page.body
        ]
        self._add_pagination(keyboard=self._keyboard_list[-1])

    @property
    def keyboard(self) -> List[InlineKeyboardMarkup]:
        self._create_all()
        return [InlineKeyboardMarkup(keyboard) for keyboard in self._keyboard_list]
