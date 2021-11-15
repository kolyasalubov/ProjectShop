import dotenv
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
from handlers.product_manager import (
    ProposeTypeSearch,
    ProposeCategories,
    ProductStates,
    CategoryTurnPage,
    AskForQuery,
    SearchByCategory,
    SearchByQuery,
    TurnProductPage,
    ProductDescription,
    ProductDescriptionBack,
)

from handlers.profile_manager import (
    ProfileStates,
    StartRegister,
    GetContact,
    EmailFilter,
    GetEmail,
    GetTelegramName,
    AskManualName,
    RegisterUser,
    ModifyUser,
    AskForName,
    AskBirthDate,
    UpdateName,
    UpdateManualName,
    DateFilter,
    SetBirthDate,
    IncorrectValue,
    ModifyManualName,
)
from handlers.user_menu import get_base_reply_keyboard

dotenv.load_dotenv("../.env")


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
                MessageHandler(Filters.text("Go to products"), ProposeTypeSearch())
            ],
            states={
                ProductStates.SEARCH: [
                    CallbackQueryHandler(
                        ProposeCategories(),
                        pattern=r"search=Search by category",
                    ),
                    CallbackQueryHandler(
                        AskForQuery(), pattern=r"search=Search by name"
                    ),
                ],
                ProductStates.CATEGORY: [
                    CallbackQueryHandler(SearchByCategory(), pattern="category="),
                    CallbackQueryHandler(
                        CategoryTurnPage(),
                        pattern=r"url=",
                    ),
                ],
                ProductStates.NAME: [MessageHandler(Filters.text, SearchByQuery())],
                ProductStates.PRODUCTS: [
                    CallbackQueryHandler(ProductDescription(), pattern=r"Description="),
                    CallbackQueryHandler(TurnProductPage(), pattern=r"url="),
                ],
                ProductStates.DESCRIPTION: [
                    CallbackQueryHandler(ProductDescriptionBack(), pattern=r".+=Back")
                ],
            },
            fallbacks=[],
        )
    )
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text("Register"), StartRegister()),
            ],
            states={
                ProfileStates.PHONE: [MessageHandler(Filters.contact, GetContact())],
                ProfileStates.EMAIL: [MessageHandler(EmailFilter(), GetEmail())],
                ProfileStates.NAME: [
                    MessageHandler(
                        Filters.text("Use telegram ones"),
                        GetTelegramName(),
                    ),
                    MessageHandler(Filters.text("Enter yourself"), AskManualName()),
                ],
                ProfileStates.MANUAL_NAME: [
                    MessageHandler(Filters.regex(r"^\w+\s+\w+"), RegisterUser())
                ],
            },
            fallbacks=[MessageHandler(Filters.all, IncorrectValue())],
        )
    )
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                MessageHandler(Filters.text("Manage profile"), ModifyUser()),
            ],
            states={
                ProfileStates.UPDATE: [
                    MessageHandler(Filters.text("Name"), AskForName()),
                    MessageHandler(Filters.text("Birth date"), AskBirthDate()),
                ],
                ProfileStates.NAME: [
                    MessageHandler(Filters.text("Use telegram ones"), UpdateName()),
                    MessageHandler(Filters.text("Enter yourself"), ModifyManualName()),
                ],
                ProfileStates.MANUAL_NAME: [
                    MessageHandler(Filters.regex(r"^\w+\s+\w+"), UpdateManualName())
                ],
                ProfileStates.BIRTH_DATE: [
                    MessageHandler(DateFilter(), SetBirthDate())
                ],
            },
            fallbacks=[MessageHandler(Filters.all, IncorrectValue())],
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
