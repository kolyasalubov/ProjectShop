import telegram
from telegram import Update
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler,
)

from TOKEN import TELEGRAM_TOKEN
from handlers.user_menu import get_base_reply_keyboard
from client.models import Category, Subcategory, Tag
from handlers.product_manager import (
    CategoryCallbacks,
    SubcategoryCallbacks,
    TagCallbacks,
    ProductCallbacks,
    CATEGORY,
    SEARCH,
    SUBCATEGORIES,
    TAGS,
    close_products,
    PRODUCTS,
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
            entry_points=[
                MessageHandler(
                    Filters.text("search products"), CategoryCallbacks.propose_page
                )
            ],
            states={
                CATEGORY: [
                    CallbackQueryHandler(
                        CategoryCallbacks.chosen_category, pattern=Category
                    ),
                    CallbackQueryHandler(
                        CategoryCallbacks.turn_page,
                        pattern=r"^http://.+/categories/.+$",
                    ),
                ],
                SEARCH: [
                    CallbackQueryHandler(
                        SubcategoryCallbacks.propose_page,
                        pattern=r"search=Apply-filters",
                    ),
                    CallbackQueryHandler(
                        ProductCallbacks.first_page, pattern=r"search=Most-popular"
                    ),
                ],
                SUBCATEGORIES: [
                    CallbackQueryHandler(
                        SubcategoryCallbacks.chosen_value, pattern=Subcategory
                    ),
                    CallbackQueryHandler(
                        SubcategoryCallbacks.turn_page,
                        pattern=r"^http://.+/subcategories/.+$",
                    ),
                    CallbackQueryHandler(
                        TagCallbacks.propose_page,
                        pass_chat_data=True,
                        pattern=r"^finish-Subcategory",
                    ),
                ],
                TAGS: [
                    CallbackQueryHandler(TagCallbacks.chosen_value, pattern=Tag),
                    CallbackQueryHandler(
                        TagCallbacks.turn_page,
                        pass_chat_data=True,
                        pattern=r"^http://.+/tags/.+$",
                    ),
                    CallbackQueryHandler(
                        ProductCallbacks.first_page,
                        pass_chat_data=True,
                        pattern=r"finish-Tag",
                    ),
                ],
                PRODUCTS: [
                    CallbackQueryHandler(
                        ProductCallbacks.turn_page, pattern=r"^http://.+/products/.+$"
                    )
                ],
            },
            fallbacks=[CommandHandler("cancel", close_products)],
        )
    )
    return dp


def run_pooling():
    """Run bot in pooling mode"""

    updater = Updater(TELEGRAM_TOKEN, use_context=True, arbitrary_callback_data=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling()
    updater.idle()
