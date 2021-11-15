from dataclasses import dataclass
from enum import Enum

from telegram import Update
from telegram.ext import CallbackContext

from interfaces.callback_items import IDataSaver
from callbacks.exceptions import NameFieldError


class ContactData(Enum):
    phone_number = "phone number"
    name = "name"


class BaseMessageSaver(IDataSaver):
    def save(self, context: CallbackContext, name: str, value: object):
        if "memory" not in context.chat_data:
            context.chat_data["memory"] = {}
        elif name in context.chat_data["memory"]:
            raise NameFieldError(name)


class UpdateMessageSaver(BaseMessageSaver):
    def save(self, context: CallbackContext, name: str, value: Update):
        super().save(context, name, value)

        if value.callback_query:
            to_save = value.callback_query.data
        else:
            to_save = value.message.text

        context.chat_data["memory"][name] = to_save


@dataclass
class ContactSaver(BaseMessageSaver):
    save_type: ContactData

    def save(self, context: CallbackContext, name: str, value: Update):
        super().save(context, name, value)

        if self.save_type == ContactData.phone_number:
            to_save = value.message.contact.phone_number
        elif self.save_type == ContactData.name:
            to_save = f"{value.message.from_user.first_name} {value.message.from_user.last_name}"

        context.chat_data["memory"][name] = to_save


class ChatDataSaver(BaseMessageSaver):
    def save(self, context: CallbackContext, name: str, value: object):
        super().save(context, name, value)
        context.chat_data["memory"][name] = value
