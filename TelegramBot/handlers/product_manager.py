from time import time

from telegram import Update
from telegram.ext import CallbackContext

from client.models import Category, Page, Subcategory, Tag
from handlers.utils import KeyboardBuilder


class PageCallbacks:
    """
    Base class for all models, that require a list of buttons.
    Implementation require only a specification of return_class.
    """
    return_class = None
    text = ""

    @classmethod
    def _build_keyboard(cls, page: Page) -> KeyboardBuilder:
        print(cls.return_class.__name__)
        keyboard_builder = KeyboardBuilder(page=page, data=f"{cls.return_class.__name__}")
        keyboard_builder.create_keyboard()
        return keyboard_builder

    @classmethod
    def propose_page(cls, update: Update, context: CallbackContext):
        """
        Callback function for creating keyboard lists. Returns to bot InlineKeyboard with first page of values
        """
        page = cls.return_class.get()
        last_message = update.message or update.callback_query.message
        message = context.bot.send_message(
            chat_id=last_message.chat_id,
            text=cls.text,
            reply_markup=cls._build_keyboard(page).keyboard
        )
        context.bot.delete_message(chat_id=last_message.chat_id, message_id=last_message.message_id)

        #       if user has already a list of specific vales, it is deleted from chat
        if f"{cls.return_class.__name__}_list" in context.chat_data:
            context.bot.delete_message(
                chat_id=update.message.chat_id,
                message_id=context.chat_data[f"{cls.return_class.__name__}_list"],
            )

        #       after that, we are saving id of message in bot's memory
        context.chat_data[f"{cls.return_class.__name__}_list"] = message.message_id

    @classmethod
    def turn_page(cls, update: Update, context: CallbackContext):
        """
        Callback function for CallbackQueryHandler with path for turning pages.
        """
        page = cls.return_class.turn_page(url=update.callback_query.data)
        context.bot.edit_message_reply_markup(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            reply_markup=cls._build_keyboard(page).keyboard,
        )


class CategoryCallbacks(PageCallbacks):
    return_class = Category
    text = "Choose category:"


class SubcategoryCallbacks(PageCallbacks):
    return_class = Subcategory
    text = "Choose subcategories for filter:"

    @classmethod
    def _build_keyboard(cls, page: Page) -> KeyboardBuilder:
        keyboard_builder = super()._build_keyboard(page)
        keyboard_builder.add_finish_button()
        return keyboard_builder


class TagCallbacks(PageCallbacks):
    return_class = Tag
    text = "Choose tags for filter:"

    @classmethod
    def _build_keyboard(cls, page: Page) -> KeyboardBuilder:
        keyboard_builder = super()._build_keyboard(page)
        keyboard_builder.add_finish_button()
        return keyboard_builder


def chosen_category(update: Update, context: CallbackContext):
    """
    Callback function for CallbackQueryHandler. After user chose category, he is asked if he wants to apply filters
    """
    context.bot.delete_message(
        chat_id=update.callback_query.message.chat_id,
        message_id=context.chat_data["Category_list"],
    )
    del context.chat_data["Category_list"]
    context.chat_data["chosen_category"] = update.callback_query.data.replace(
        "category=", ""
    )
    keyboard_builder = KeyboardBuilder(Page(results=["Yes", "No"]), "filters")
    keyboard_builder.create_keyboard(columns=2)
    context.bot.send_message(
        chat_id=update.callback_query.message.chat_id,
        text="Do you want to apply any filters?",
        reply_markup=keyboard_builder.keyboard
    )


def filters_subcategories(update: Update, context: CallbackContext):
    """
    Callback function for applying filters. One for subcategories
    """
