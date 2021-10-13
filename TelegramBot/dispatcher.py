import telegram
from telegram.ext import (
    Updater, Filters,
    CommandHandler, MessageHandler, CallbackQueryHandler,
)

from TOKEN import TELEGRAM_TOKEN
from handlers.product_manager import chosen_category, CategoryCallbacks, \
    SubcategoryCallbacks, TagCallbacks
from handlers.user_menu import BUTTON_SHOW_PRODUCTS, get_base_reply_keyboard


def start_command(update, context):
    """ This is start command for user """
    update.message.reply_text(
        text="This is your shopping bot",
        reply_markup=get_base_reply_keyboard(),
    )


def setup_dispatcher(dp):
    """ Setupping dispatcher and adding all handlers """
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(MessageHandler(Filters.text('search products'), CategoryCallbacks.propose_page, pass_chat_data=True))
    dp.add_handler(CallbackQueryHandler(CategoryCallbacks.turn_page, pass_chat_data=True,
                                        pattern=r'^http://.+/categories/.+$'))
    dp.add_handler(CallbackQueryHandler(chosen_category, pass_chat_data=True,
                                        pattern=r'Category=.+'))
    dp.add_handler(CallbackQueryHandler(SubcategoryCallbacks.propose_page, pass_chat_data=True,
                                        pattern=r"filters=Yes"))
    dp.add_handler(CallbackQueryHandler(SubcategoryCallbacks.turn_page, pass_chat_data=True,
                                        pattern=r'^http://.+/subcategories/.+$'))
    dp.add_handler(CallbackQueryHandler(TagCallbacks.propose_page, pass_chat_data=True,
                                        pattern=r'^finish-Subcategory'))
    dp.add_handler(CallbackQueryHandler(TagCallbacks.turn_page, pass_chat_data=True,
                                        pattern=r'^http://.+/tags/.+$'))
    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Pooling of '{bot_link}' started")
    updater.start_polling()
    updater.idle()


