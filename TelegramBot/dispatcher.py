import telegram
from telegram import Update, ParseMode
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    CallbackContext,
    Defaults,
)

from TOKEN import TELEGRAM_TOKEN
from client.models import Category, Product
from handlers.product_manager import (
    CategoryCallbacks,
    ProductCallbacks,
    ProductStates,
    search_type,
    name_search,
    close_products,
)
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
from handlers.user_menu import get_base_reply_keyboard


def start_command(update: Update, _: CallbackContext):
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
    dp.add_handler(
        ConersationHandler(
            entry_points=[MessageHandler(Filters.text("Go to products"), search_type)],
            states={
                ProductStates.SEARCH: [
                    CallbackQueryHandler(
                        CategoryCallbacks.propose_page,
                        pattern=r"search=Search-by-category",
                    ),
                    CallbackQueryHandler(name_search, pattern=r"search=Search-by-name"),
                ],
                ProductStates.CATEGORY: [
                    CallbackQueryHandler(ProductCallbacks.first_page, pattern=Category),
                    CallbackQueryHandler(
                        CategoryCallbacks.turn_page,
                        pattern=r"^http://.+/categories/.+$",
                    ),
                ],
                ProductStates.NAME: [
                    MessageHandler(Filters.text, ProductCallbacks.first_page)
                ],
                ProductStates.PRODUCTS: [
                    CallbackQueryHandler(ProductCallbacks.description, pattern=Product),
                    CallbackQueryHandler(
                        ProductCallbacks.turn_page, pattern=r"^http://.+/products/.+$"
                    ),
                ],
                ProductStates.DESCRIPTION: [
                    CallbackQueryHandler(
                        ProductCallbacks.go_back, pattern=r"product=Back"
                    )
                ],
            },
            fallbacks=[CommandHandler("cancel", close_products)],
        )
    )
    return dp


def run_pooling():
    """Run bot in pooling mode"""

    defaults = Defaults(parse_mode=ParseMode.MARKDOWN_V2)

    updater = Updater(
        TELEGRAM_TOKEN,
        defaults=defaults,
        use_context=True,
        arbitrary_callback_data=True,
    )

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling()
    updater.idle()
