from __future__ import annotations

from telegram import Update, Message, Bot
from telegram.ext import CallbackContext
from typing import Iterable

from callbacks.message_history_managers import MessageHistoryManager
from interfaces.callback_items import (
    ISchema,
    IDataLoader,
    IDataSaver,
    IMessageHistoryManager,
    IMenuBuilder,
    ICallbackClass,
    IMessageBuilder,
    IMessageAlter,
    IMessageRebuilder,
)


class BaseCallback(ICallbackClass):
    schema: ISchema
    message: type(IMessageBuilder) | Iterable[type(IMessageBuilder)]
    menu: type(IMenuBuilder) | Iterable[type(IMenuBuilder)] = None
    name: str = None
    save: IDataSaver = None
    load: Iterable[IDataLoader] | IDataLoader = None
    delete: str | Iterable[str] = None
    history_manager: IMessageHistoryManager = MessageHistoryManager()
    state: int = None

    def _normalize_attributes(self):
        if isinstance(self.load, IDataLoader):
            self.load = (self.load,)
        if not isinstance(self.message, Iterable):
            self.message = (self.message,)
        if not isinstance(self.menu, Iterable):
            self.menu = (self.menu,)

    def _clean_up_chat(self, update: Update, context: CallbackContext):
        if self.delete:
            [
                self.history_manager.delete(update, context, delete)
                for delete in self.delete
            ]

    def _save_data(self, update: Update, context: CallbackContext):
        if self.save:
            self.save.save(context=context, name=self.name, value=update)

    def command(self, update: Update, context: CallbackContext):
        pass

    def _load_data(self, update: Update, context: CallbackContext):
        if self.load:
            self.data = {}
            for data_loader in self.load:
                self.data.update(data_loader.load(update, context))
            print("4.1")
            self.schema.load_data(self.data)
            print("4.2")

    def _init_menu(self):
        if self.schema.keyboard:
            self._menu_instance = [
                menu(**self.schema.keyboard) if menu else None for menu in self.menu
            ]
        else:
            self._menu_instance = [menu() if menu else None for menu in self.menu]

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class MessageCallback(BaseCallback):
    def _normalize_attributes(self):
        super()._normalize_attributes()
        if isinstance(self.delete, str):
            self.delete = (self.delete,)

    def _send_message(self, update: Update, context: CallbackContext):
        update_message = update.message or update.callback_query.message
        message = [
            message(
                bot=context.bot,
                chat_id=update_message.chat_id,
                menu_builder=menu_instance,
            ).send(self.schema.message)
            for message, menu_instance in zip(self.message, self._menu_instance)
        ]

        self.history_manager.save(context, self.name, message)

    def __call__(self, update: Update, context: CallbackContext):
        self._normalize_attributes()
        self._save_data(update, context)
        self._load_data(update, context)
        self._init_menu()
        self._clean_up_chat(update, context)
        self._send_message(update, context)
        self.command(update, context)
        return self.state


class EditMessageCallback(BaseCallback):
    edit: str
    message: type(IMessageAlter) | Iterable[type(IMessageAlter)]

    def _load_message(self, context: CallbackContext) -> Message | Iterable[Message]:
        return self.history_manager.load(context, self.edit)

    def _edit_message(self, message: Message | Iterable[Message]):
        if isinstance(message, Message):
            message = (message,)

        [
            message_builder(message=message_instance, menu_builder=menu_instance).edit()
            for message_builder, message_instance, menu_instance in zip(
                self.message, message, self._menu_instance
            )
        ]

    def __call__(self, update: Update, context: CallbackContext):
        self._normalize_attributes()
        self._save_data(update, context)
        self._load_data(update, context)
        self._init_menu()
        self._edit_message(self._load_message(context))
        self.command(update, context)
        return self.state


class ReturnMessageCallback(BaseCallback):
    delete: Iterable[str] | str = None
    return_message: str | Iterable[str]
    message: type(IMessageRebuilder)

    def _normalize_attributes(self):
        super()._normalize_attributes()
        if isinstance(self.delete, str):
            self.delete = (self.delete,)
        if isinstance(self.return_message, str):
            self.return_message = (self.return_message,)

    def _init_message_builder(self, bot: Bot):
        self._message_builder = self.message[0](bot)

    def _load_history(self, context: CallbackContext):
        self.deleted_messages = [
            self.history_manager.load(context, message_name)
            for message_name in self.return_message
        ]

    def _return_message(self, message: Message | Iterable):
        if isinstance(message, Iterable):
            for message_part in message:
                self._return_message(message_part)
        else:
            self.sent_messages.append(self._message_builder.send(message))

    def _change_history(self, update: Update, context: CallbackContext):
        for name in self.return_message:
            self.history_manager.clean(context, name)
        self.history_manager.save(context, self.name, self.sent_messages)

    def __call__(self, update: Update, context: CallbackContext):
        self._normalize_attributes()
        self._save_data(update, context)
        self._load_data(update, context)
        self._load_history(context)
        self._init_message_builder(context.bot)
        self._clean_up_chat(update, context)
        self.sent_messages = []
        self._return_message(self.deleted_messages)
        self._change_history(update, context)
        self.command(update, context)
        return self.state
