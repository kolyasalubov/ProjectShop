import re
from enum import Enum

from telegram import Message
from telegram.ext import MessageFilter, ConversationHandler

from callbacks.callbacks import MessageCallback
from callbacks.data_loaders import (
    RegisterUserLoader,
    ChatDataLoader,
    UpdateUserLoader,
    TelegramIdLoader,
)
from callbacks.data_savers import (
    ContactSaver,
    ContactData,
    UpdateMessageSaver,
    ChatDataSaver,
)
from callbacks.menu_builders import ReplyKeyboardBuilder, RemoveReplyKeyboard
from callbacks.message_builders import MessageBuilder
from callbacks.schemas import BaseSchema


class ProfileStates(Enum):
    PHONE, EMAIL, NAME, MANUAL_NAME, UPDATE, BIRTH_DATE = range(6)


class EmailFilter(MessageFilter):
    """
    Filter to accept Emails only
    """

    pattern = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")

    def filter(self, message: Message) -> bool:
        return bool(re.match(self.pattern, message.text))


class DateFilter(MessageFilter):
    """
    Filter to accept Dates only in the format 'YYYY-MM-DD'
    """

    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}")

    def filter(self, message: Message) -> bool:
        return bool(re.match(self.pattern, message.text))


class StartRegister(MessageCallback):
    name = "register_start"
    delete = "update"
    schema = BaseSchema("ask_for_phone_number")
    menu = ReplyKeyboardBuilder
    message = MessageBuilder
    state = ProfileStates.PHONE


class GetContact(MessageCallback):
    name = "phone_number"
    delete = ["update", "register_start"]
    save = ContactSaver(ContactData.phone_number)
    schema = BaseSchema("ask_for_email")
    menu = RemoveReplyKeyboard
    message = MessageBuilder
    state = ProfileStates.EMAIL


class AskForName(MessageCallback):
    name = "asK_name"
    schema = BaseSchema("ask_for_name")
    menu = ReplyKeyboardBuilder
    message = MessageBuilder
    state = ProfileStates.NAME


class GetEmail(AskForName):
    name = "email"
    delete = ["update", "phone_number"]
    save = UpdateMessageSaver()


class AskManualName(MessageCallback):
    name = "manual_name"
    delete = ["update", "email"]
    schema = BaseSchema("ask_for_manual_name")
    menu = RemoveReplyKeyboard
    message = MessageBuilder
    state = ProfileStates.MANUAL_NAME


class ModifyManualName(AskManualName):
    delete = ["update", "ask_name"]


class RegisterUser(MessageCallback):
    name = "name"
    delete = ["update", "manual_name"]
    save = UpdateMessageSaver()
    load = RegisterUserLoader(
        [ChatDataLoader(["phone_number", "email", "name"]), TelegramIdLoader()]
    )
    schema = BaseSchema("registration_success")
    message = MessageBuilder
    state = ConversationHandler.END

    def command(self, update, context):
        ChatDataSaver().save(context, "user", self.data["user"])


class GetTelegramName(RegisterUser):
    delete = ["update", "email"]
    save = ContactSaver(ContactData.name)
    menu = RemoveReplyKeyboard


class ModifyUser(MessageCallback):
    name = "modify_user"
    delete = "update"
    schema = BaseSchema("ask_for_update")
    menu = ReplyKeyboardBuilder
    message = MessageBuilder
    state = ProfileStates.UPDATE


class AskBirthDate(MessageCallback):
    name = "ask_birth_date"
    delete = ["update", "modify_user"]
    schema = BaseSchema("ask_for_birth_date")
    menu = RemoveReplyKeyboard
    message = MessageBuilder
    state = ProfileStates.BIRTH_DATE


class SetBirthDate(MessageCallback):
    name = "birth_date"
    delete = ["update", "ask_birth_date"]
    save = UpdateMessageSaver()
    load = UpdateUserLoader(ChatDataLoader(["birth_date"]))
    schema = BaseSchema("modify_birth_date_success")
    message = MessageBuilder
    state = ConversationHandler.END


class UpdateManualName(MessageCallback):
    name = "name"
    delete = ["update", "manual_name"]
    save = UpdateMessageSaver()
    load = UpdateUserLoader(ChatDataLoader(["name"]))
    schema = BaseSchema("modify_name_success")
    message = MessageBuilder
    state = ConversationHandler.END


class UpdateName(UpdateManualName):
    delete = ["update", "ask_name"]
    save = ContactSaver(ContactData.name)
    menu = RemoveReplyKeyboard


class IncorrectValue(MessageCallback):
    name = "incorrect"
    delete = "update"
    schema = BaseSchema("incorrect_value")
    message = MessageBuilder

    def command(self, update, context):
        self.history_manager.delete_with_interval(context, "incorrect", 10)
