import telegram
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

from TOKEN import TELEGRAM_TOKEN
from handlers.profile_manager import (
    RegisterCallbacks,
    PHONE,
    EMAIL,
    NAME,
    MANUAL_NAME,
    EmailFilter,
    ProfileCallbacks,
    UpdateCallbacks,
    UPDATE,
    BIRTH_DATE,
    DateFilter,
)
from handlers.user_menu import get_base_reply_keyboard


def start_command(update, context):
    """This is start command for user"""

    update.message.reply_text(
        text="This is your shopping bot",
        reply_markup=get_base_reply_keyboard(),
    )


def setup_dispatcher(dp):
    """Setupping dispatcher and adding all handlers"""

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text("Register"), RegisterCallbacks.register),
            ],
            states={
                PHONE: [MessageHandler(Filters.contact, RegisterCallbacks.ask_email)],
                EMAIL: [MessageHandler(EmailFilter(), RegisterCallbacks.get_email)],
                NAME: [
                    MessageHandler(
                        Filters.text("Use telegram ones"),
                        RegisterCallbacks.telegram_name,
                    ),
                    MessageHandler(
                        Filters.text("Enter yourself"), ProfileCallbacks.enter_name
                    ),
                ],
                MANUAL_NAME: [
                    MessageHandler(
                        Filters.regex(r"^\w+\s+\w+"), RegisterCallbacks.get_name
                    )
                ],
            },
            fallbacks=[MessageHandler(Filters.all, ProfileCallbacks.incorrect_value)],
        )
    )
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text("Manage profile"), UpdateCallbacks.patch),
            ],
            states={
                UPDATE: [
                    MessageHandler(Filters.text("Name"), ProfileCallbacks.ask_name),
                    MessageHandler(
                        Filters.text("Birth date"), UpdateCallbacks.ask_birth_date
                    ),
                ],
                NAME: [
                    MessageHandler(
                        Filters.text("Use telegram ones"), UpdateCallbacks.telegram_name
                    ),
                    MessageHandler(
                        Filters.text("Enter yourself"), ProfileCallbacks.enter_name
                    ),
                ],
                MANUAL_NAME: [
                    MessageHandler(
                        Filters.regex(r"^\w+\s+\w+"), UpdateCallbacks.get_name
                    )
                ],
                BIRTH_DATE: [
                    MessageHandler(DateFilter, UpdateCallbacks.get_birth_date)
                ],
            },
            fallbacks=[MessageHandler(Filters.all, ProfileCallbacks.incorrect_value)],
        )
    )
    return dp


def run_pooling():
    """Run bot in pooling mode"""

    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = "https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling()
    updater.idle()
