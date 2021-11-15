from dataclasses import dataclass

from typing import List, Union

from telegram import Message, Bot, InputMediaPhoto
from telegram.utils.helpers import escape_markdown

from interfaces.callback_items import (
    IMessageBuilder,
    IMessageAlter,
    IMenuBuilder,
    IMessageRebuilder,
)
from callbacks.menu_builders import MessageMenuBuilder


@dataclass
class MessageKeyboardEditor(IMessageAlter):
    menu_builder: IMenuBuilder
    message: Message

    @property
    def reply_markup(self):
        return self.menu_builder.keyboard

    def edit(self):
        self.message.edit_reply_markup(reply_markup=self.reply_markup)


@dataclass
class BaseMessageBuilder(IMessageBuilder):
    bot: Bot
    chat_id: Union[int, str]
    menu_builder: IMenuBuilder

    @property
    def reply_markup(self):
        return self.menu_builder.keyboard if self.menu_builder else None

    def send(self, data: dict) -> Union[Message, List[Message]]:
        raise NotImplementedError


@dataclass
class MessageBuilder(BaseMessageBuilder):
    def send(self, data: dict) -> Message:
        return self.bot.send_message(
            chat_id=self.chat_id, text=data["text"], reply_markup=self.reply_markup
        )


@dataclass
class AlbumBuilder(BaseMessageBuilder):
    def send(self, data: Message) -> Message:
        open_images = [*map(lambda image: InputMediaPhoto(image.get()), data["media"])]
        return self.bot.send_media_group(chat_id=self.chat_id, media=open_images)


@dataclass
class PageMessageGroupBuilder(BaseMessageBuilder):
    menu_builder: MessageMenuBuilder

    def send(self, data: List) -> List[Message]:
        open_images = map(lambda schema: schema["image"].get(), data)
        text_list = map(lambda schema: schema["caption"], data)
        return [
            self.bot.send_photo(
                chat_id=self.chat_id,
                photo=image,
                caption=text,
                reply_markup=reply_markup,
            )
            for image, text, reply_markup in zip(
                open_images, text_list, self.reply_markup
            )
        ]


@dataclass
class PhotoMessageRebuilder(IMessageRebuilder):
    bot: Bot

    def send(self, message: Message) -> Union[Message, List[Message]]:
        chat_id = message.chat_id
        photo = message.photo[0]
        caption = message.caption
        reply_markup = message.reply_markup
        return self.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=escape_markdown(caption, version=2),
            reply_markup=reply_markup,
        )
