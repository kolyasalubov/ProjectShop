from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from client.models import Category, Page, Subcategory, Tag, Product
from handlers.utils import KeyboardBuilder

# constants for conversation states
CATEGORY, SEARCH, SUBCATEGORIES, TAGS, PRODUCTS = range(5)


class PageCallbacks:
    """
    Base class for all models, that require a list of buttons.
    Implementation require only a specification of return_class.
    """

    return_class = None
    text = ""
    propose_state = 0

    @classmethod
    def _build_keyboard(cls, page: Page) -> KeyboardBuilder:
        keyboard_builder = KeyboardBuilder(page=page)
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
            reply_markup=cls._build_keyboard(page).keyboard,
        )
        last_message.delete()

        #       if user has already a list of specific values, it is deleted from chat
        if f"{cls.return_class.__name__}_list" in context.chat_data:
            context.chat_data[f"{cls.return_class.__name__}_list"].delete()

        #       after that, we are saving the message in bot's memory
        context.chat_data[f"{cls.return_class.__name__}_list"] = message
        return cls.propose_state

    @classmethod
    def turn_page(cls, update: Update, _: CallbackContext):
        """
        Callback function for CallbackQueryHandler with path for turning pages.
        """
        page = cls.return_class.turn_page(url=update.callback_query.data)
        update.callback_query.edit_message_reply_markup(
            reply_markup=cls._build_keyboard(page).keyboard,
        )


class FilterCallbacks(PageCallbacks):
    """
    Base class for models, that are used as filters
    """

    @classmethod
    def _build_keyboard(cls, page: Page) -> KeyboardBuilder:
        keyboard_builder = super()._build_keyboard(page)
        keyboard_builder.add_finish_button(data=cls.return_class.__name__)
        return keyboard_builder

    @classmethod
    def chosen_value(cls, update: Update, context: CallbackContext):
        query = update.callback_query
        reply_markup = query.message.reply_markup
        if cls.return_class not in context.chat_data:
            context.chat_data[cls.return_class] = []
        filters = context.chat_data[cls.return_class]
        if query.data in filters:
            query.answer(f"'{query.data}' has been removed from filters!")
            filters.remove(query.data)
        else:
            query.answer(f"'{query.data}' has been added to filters!")
            filters.append(query.data)
        query.edit_message_text(
            text=cls.text + "\n" + "\n".join(map(str, filters)),
            reply_markup=reply_markup,
        )


class CategoryCallbacks(PageCallbacks):
    return_class = Category
    text = "Choose category:"
    propose_state = CATEGORY

    @classmethod
    def chosen_category(cls, update: Update, context: CallbackContext):
        """
        Callback function for CallbackQueryHandler. After user chose category, he is asked if he wants to apply filters
        """
        context.chat_data[f"{cls.return_class.__name__}_list"].delete()

        del context.chat_data[f"{cls.return_class.__name__}_list"]

        context.chat_data[Category] = update.callback_query.data

        keyboard_builder = KeyboardBuilder(
            Page(results=["Apply filters", "Search by name", "Most popular"]), "search"
        )
        keyboard_builder.create_keyboard(columns=3)
        context.bot.send_message(
            chat_id=update.callback_query.message.chat_id,
            text="What type of search would you like?",
            reply_markup=keyboard_builder.keyboard,
        )
        return SEARCH


class SubcategoryCallbacks(FilterCallbacks):
    return_class = Subcategory
    text = "Choose subcategories for filter:"
    propose_state = SUBCATEGORIES


class TagCallbacks(FilterCallbacks):
    return_class = Tag
    text = "Choose tags for filter:"
    propose_state = TAGS


class ProductCallbacks:
    @staticmethod
    def product_list(update: Update, context: CallbackContext):
        """
        Function for viewing product list. Visualization is different from previous examples
        """
        update.callback_query.delete_message()

        page = Product.view_products(
            category=context.chat_data[Category],
            subcategories=context.chat_data[Subcategory],
            tags=context.chat_data[Tag],
        )
        for product in page.results:
            keyboard_builder = KeyboardBuilder(
                Page(results=["description"]), product.name
            ).create_keyboard()
            message = context.bot.send_message(
                chat_id=update.callback_query.message.chat_id,
                caption=product.name,
                image=product.image[0],
                reply_markup=keyboard_builder.keyboard,
            )


def close_products(update: Update, context: CallbackContext):
    update.message.reply_text(text="Canceling product search!")
    del context.chat_data[Category]
    del context.chat_data[Subcategory]
    del context.chat_data[Tag]
    return ConversationHandler.END
