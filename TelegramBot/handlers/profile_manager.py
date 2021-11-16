import re
from datetime import date

from telegram import Update, Message
from telegram.ext import CallbackContext, MessageFilter, ConversationHandler

from client.models import User
from handlers.user_menu import get_base_reply_keyboard
from handlers.utils import KeyboardBuilder, delete_message

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


class ProfileCallbacks:
    """
    Callbacks that are the same in both conversations
    """

    @staticmethod
    def ask_name(update: Update, context: CallbackContext):
        """
        Asks user if they want to use telegram names, or entered themselves
        """
        keyboard = KeyboardBuilder(["Use telegram ones", "Enter yourself"])
        message = context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Good, now we need your first- and lastname. Would you like to use the ones from your account or enter them yourself?",
            reply_markup=keyboard.create(columns=2),
        )
        context.chat_data["delete"] = message

        return NAME

    @staticmethod
    def enter_name(update: Update, context: CallbackContext):
        """
        Asks user to type in first- and lastname
        """
        update.message.delete()
        context.chat_data["delete"].delete()

        message = context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Please, enter your firstname and lastname (in that exact order):",
            reply_markup=KeyboardBuilder.remove(),
        )
        context.chat_data["delete"] = message

        return MANUAL_NAME

    @staticmethod
    def incorrect_value(update: Update, context: CallbackContext):
        """
        Message shows up each time an incorrect value for the exact moment is sent
        """
        update.message.delete()

        message = context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Your input is incorrect, try again",
        )

        context.job_queue.run_once(delete_message, when=10, context=message)


class RegisterCallbacks:
    """Callbacks fot registration conversation"""

    @staticmethod
    def register(update: Update, context: CallbackContext):
        """Entry point. Saves user's telegram id and asks for phone number"""
        update.message.delete()

        context.chat_data["register"] = {"telegram_id": update.message.chat_id}

        keyboard = KeyboardBuilder(
            ["Share phone number"], request_contact="Share phone number"
        )
        message = context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Please, share your phone number:",
            reply_markup=keyboard.create(),
        )
        context.chat_data["delete"] = message

        return PHONE

    @staticmethod
    def ask_email(update: Update, context: CallbackContext):
        """
        Saves phone number and asks for email
        """
        update.message.delete()
        context.chat_data["delete"].delete()

        context.chat_data["register"][
            "phone_number"
        ] = update.message.contact.phone_number

        message = context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Good, now we need your email:",
            reply_markup=KeyboardBuilder.remove(),
        )
        context.chat_data["delete"] = message

        return EMAIL

    @staticmethod
    def get_email(update: Update, context: CallbackContext):
        """
        Saves email and calls ProfileCallbacks.ask_name
        """
        update.message.delete()
        context.chat_data["delete"].delete()

        context.chat_data["register"]["email"] = update.message.text

        return ProfileCallbacks.ask_name(update, context)

    @staticmethod
    def telegram_name(update: Update, context: CallbackContext):
        """
        Saves first- and lastname from user info and submits him to server
        """
        update.message.delete()
        context.chat_data["delete"].delete()

        context.chat_data["register"][
            "first_name"
        ] = update.message.from_user.first_name
        context.chat_data["register"]["last_name"] = update.message.from_user.last_name
        context.chat_data["user"] = User.register_user(**context.chat_data["register"])
        del context.chat_data["register"]

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Thank you! Now, you are a registered user!",
            reply_markup=get_base_reply_keyboard(),
        )

        return ConversationHandler.END

    @staticmethod
    def get_name(update: Update, context: CallbackContext):
        """
        Saves first- and lastname from input and submits them to server
        """
        update.message.delete()
        context.chat_data["delete"].delete()

        first_name, last_name = update.message.text.split()
        context.chat_data["register"]["first_name"] = first_name
        context.chat_data["register"]["last_name"] = last_name
        context.chat_data["user"] = User.register_user(**context.chat_data["register"])
        del context.chat_data["register"]

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Thank you! Now, you are a registered user!",
            reply_markup=get_base_reply_keyboard(),
        )

        return ConversationHandler.END


class UpdateCallbacks:
    """
    Callbacks regarding updating profile info
    """

    @staticmethod
    def patch(update: Update, context: CallbackContext):
        """
        Entry point. Asks what has to be updated, if user is registered
        """
        update.message.delete()

        if "user" not in context.chat_data:
            message = context.bot.send_message(
                chat_id=update.message.chat_id,
                text="You haven't registered yet! What you want to manage? Onions?",
            )

            context.job_queue.run_once(delete_message, when=10, context=message)

            return ConversationHandler.END

        keyboard = KeyboardBuilder(["Name", "Birth date"])
        message = context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Now, what information about yourself you would like to add/update?",
            reply_markup=keyboard.create(columns=2),
        )
        context.chat_data["delete"] = message

        return UPDATE

    @staticmethod
    def telegram_name(update: Update, context: CallbackContext):
        """
        Saves first- and lastname from user info and submits him to server
        """
        update.message.delete()
        context.chat_data["delete"].delete()

        first_name = update.message.from_user.first_name
        last_name = update.message.from_user.last_name
        context.chat_data["user"] = context.chat_data["user"].update(
            first_name=first_name, last_name=last_name
        )

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Great! Now you are {first_name} {last_name}",
        )

        return ConversationHandler.END

    @staticmethod
    def get_name(update: Update, context: CallbackContext):
        """
        Saves first- and lastname from input and submits them to server
        """
        update.message.delete()
        context.chat_data["delete"].delete()

        first_name, last_name = update.message.text.split()
        context.chat_data["user"] = context.chat_data["user"].update(
            first_name=first_name, last_name=last_name
        )

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Great! Now you are {first_name} {last_name}",
        )

        return ConversationHandler.END

    @staticmethod
    def ask_birth_date(update: Update, context: CallbackContext):
        """
        Asks user for birth date in format 'YYYY-MM-DD'
        """
        update.message.delete()
        context.chat_data["delete"].delete()

        message = context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Good, please enter your birthday date in format 'YYYY-MM-DD'",
        )

        context.chat_data["delete"] = message

        return BIRTH_DATE

    @staticmethod
    def get_birth_date(update: Update, context: CallbackContext):
        """
        Gets birth date from input and submits it to server
        """
        update.message.delete()
        context.chat_data["delete"].delete()

        birth_date = date.fromisoformat(update.message.text)
        context.chat_data["user"] = context.chat_data["user"].update(
            birth_date=birth_date
        )

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Great! Now we know when to give you a present!",
        )
