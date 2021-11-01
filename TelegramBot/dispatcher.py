import telegram
from telegram import Update, ParseMode
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler,
    Defaults,
)

from TOKEN import TELEGRAM_TOKEN
from client.models import Category, Product
from handlers.product_manager import (
    search_type,
    SEARCH,
    CategoryCallbacks,
    name_search,
    CATEGORY,
    ProductCallbacks,
    NAME,
    PRODUCTS,
    close_products,
    DESCRIPTION,
)
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
            entry_points=[MessageHandler(Filters.text("search products"), search_type)],
            states={
                SEARCH: [
                    CallbackQueryHandler(
                        CategoryCallbacks.propose_page,
                        pattern=r"search=Search-by-category",
                    ),
                    CallbackQueryHandler(name_search, pattern=r"search=Search-by-name"),
                ],
                CATEGORY: [
                    CallbackQueryHandler(ProductCallbacks.first_page, pattern=Category),
                    CallbackQueryHandler(
                        CategoryCallbacks.turn_page,
                        pattern=r"^http://.+/categories/.+$",
                    ),
                ],
                NAME: [MessageHandler(Filters.text, ProductCallbacks.first_page)],
                PRODUCTS: [
                    CallbackQueryHandler(
                        ProductCallbacks.turn_page, pattern=r"^http://.+/products/.+$"
                    ),
                    CallbackQueryHandler(ProductCallbacks.description, pattern=Product),
                ],
                DESCRIPTION: [
                    CallbackQueryHandler(
                        ProductCallbacks.go_back, pattern=r"product=Go-back"
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
