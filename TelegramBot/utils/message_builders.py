from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing import Optional, List, Union

from telegram import Message, ReplyMarkup, Bot

from utils.image import IImage
from utils.menu_builders import IMenuBuilder, MessageMenuBuilder
from utils.schemas import SchematicMessage


class IMessageBuilder(ABC):
    @property
    @abstractmethod
    def reply_markup(self) -> Optional[ReplyMarkup, List[ReplyMarkup]]:
        pass

    @abstractmethod
    def send(self, bot: Bot, chat_id: Union[int, str]) -> Optional[Message, List[Message]]:
        pass


@dataclass
class BaseMessageBuilder(IMessageBuilder):
    menu_builder: IMenuBuilder
    message: Optional[SchematicMessage, List[SchematicMessage]]

    @property
    def reply_markup(self):
        return self.menu_builder.keyboard if self.menu_builder else None

    def send(self, bot: Bot, chat_id: Union[int, str]) -> Optional[Message, List[Message]]:
        return NotImplementedError


class TextMessageBuilder(BaseMessageBuilder):

    def send(self, bot: Bot, chat_id: Union[int, str]) -> Message:
        return bot.send_message(chat_id=chat_id, text=self.message.text, reply_markup=self.reply_markup)


class AlbumBuilder(BaseMessageBuilder):

    def send(self, bot: Bot, chat_id: Union[int, str]) -> Message:
        open_images = [*map(lambda image: image.get(), self.message.album)]
        return bot.send_message(chat_id=chat_id,media=open_images, reply_markup=self.reply_markup)


@dataclass
class PageMessageGroupBuilder(BaseMessageBuilder):
    menu_builder: MessageMenuBuilder
    message: List[SchematicMessage]

    def send(self, bot: Bot, chat_id: Union[int, str]) -> List[Message]:
        return [bot.send_photo(chat_id=chat_id, photo=message.image, caption=message.text) for message in self.message]
