from enum import Enum

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from telegram.utils.helpers import escape_markdown

from client.models import Category, Page, Product
from handlers.utils import KeyboardBuilder


# constants for conversation states
class ProductStates(Enum):
    SEARCH, CATEGORY, NAME, PRODUCTS, DESCRIPTION = range(5)


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
        context.bot.send_message(
            chat_id=last_message.chat_id,
            text=cls.text,
            reply_markup=cls._build_keyboard(page).keyboard,
        )

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


def search_type(update: Update, context: CallbackContext):
    """
    Callback function for CallbackQueryHandler. User is deciding what kind of search they want: by name or by category
    """

    update.message.delete()

    keyboard_builder = KeyboardBuilder(
        Page(results=["Search by category", "Search by name"]), "search"
    )
    keyboard_builder.create_keyboard(columns=2)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="What type of search would you like?",
        reply_markup=keyboard_builder.keyboard,
    )
    return ProductStates.SEARCH


def name_search(update: Update, context: CallbackContext):
    """
    Function for getting user query for product filtering/searching
    """
    update.callback_query.delete_message()

    context.bot.send_message(
        chat_id=update.callback_query.message.chat_id,
        text="Enter your search query, please:")

    return ProductStates.NAME


def close_products(update: Update, context: CallbackContext):
    """
    Function to clean memory after finishing the conversation
    """
    update.message.reply_text(text="Canceling product search!")
    del context.chat_data[Category]
    for message in context.chat_data[Product]:
        message.delete_message()
    del context.chat_data[Product]
    del context.chat_data["Product-list-cache"]
    return ConversationHandler.END


class CategoryCallbacks(PageCallbacks):
    return_class = Category
    text = "Choose category:"
    propose_state = ProductStates.CATEGORY


class ProductCallbacks:
    """
    All callbacks that are directly related with product surfing
    """

    @staticmethod
    def _get_page(update: Update, context: CallbackContext):
        """
        Function to get page of Products.
        If cached page exists, it will not make another request
        """

        if "Product-list-cache" in context.chat_data:
            return context.chat_data["Product-list-cache"]
        else:
            if update.message:
                query = update.message.text.split()
                category = None
            else:
                category = update.callback_query.data
                query = None

            product_list = Product.view_products(category=category, query=query)
            context.chat_data["Product-list-cache"] = product_list

            return product_list

    @staticmethod
    def _product_list(update: Update, context: CallbackContext):
        """
        Function for viewing product list. Visualization is different from previous examples:
        We are getting page of messages, each is photo with name of product as caption.
        Also each message has a 'description' button for opening detailed information
        We are saving all messages in chat_data, because they all have to be deleted when another callback is called
        """

        page = ProductCallbacks._get_page(update, context)
        context.chat_data[Product] = []

        for product in page.results:
            keyboard_builder = KeyboardBuilder(Page(results=[product]))
            keyboard_builder.create_keyboard(
                text="Description"
            )

            # message = context.bot.send_photo(
            #     chat_id=update.callback_query.message.chat_id,
            #     caption=escape_markdown(product.name, version=2),
            #     photo=product.images[0]["image"],
            #     reply_markup=keyboard_builder.keyboard,
            # )
            message = context.bot.send_message(
                chat_id=update.callback_query.message.chat_id,
                text=f"*{escape_markdown(product.name, version=2)}*",
                reply_markup=keyboard_builder.keyboard
            )
            context.chat_data[Product].append(message)

        #       We need to add page changing buttons to the end of the list
        page.results = page.results[-1:]
        keyboard_builder = KeyboardBuilder(page=page)
        keyboard_builder.create_keyboard(
            text="Description"
        )
        context.chat_data[Product][-1].edit_reply_markup(
            reply_markup=keyboard_builder.keyboard
        )


    @staticmethod
    def first_page(update: Update, context: CallbackContext):
        message = update.message or update.callback_query.message
        message.delete()
        ProductCallbacks._product_list(update, context)
        return ProductStates.PRODUCTS

    @staticmethod
    def turn_page(update: Update, context: CallbackContext):
        context.chat_data["Product-list-cache"] = Product.turn_page(
            update.callback_query.data
        )
        for message in context.chat_data[Product]:
            message.delete()
        ProductCallbacks._product_list(update, context)

    @staticmethod
    def description(update: Update, context: CallbackContext):
        """
        Detailed info about product
        It will send two messages, one with an album of photos, another - with description, tags, price and video link
        We have the possibility to save product to wishlist, add to cart or go back to product list
        """
        product: Product = update.callback_query.data

        # album_message = context.bot.send_media_group(
        #     chat_id=update.callback_query.message.chat_id, media=[i["image"] for i in product.images]
        # )

        keyboard_builder = KeyboardBuilder(
            Page(results=["Add to wishlist", "Add to order", "Back"]), "product"
        )
        keyboard_builder.create_keyboard()

        description_message = context.bot.send_message(
            chat_id=update.callback_query.message.chat_id,
            text=f"""
            *{escape_markdown(product.name, version=2)}*

            {escape_markdown(product.description, version=2)}
            
            _{escape_markdown(chr(9).join(str(tag) for tag in product.tags), version=2)}_

            *${escape_markdown(str(product.price), version=2)}*

            {escape_markdown(product.video_links[0]["video_link"], version=2)}""",
            reply_markup=keyboard_builder.keyboard,
        )

        for message in context.chat_data[Product]:
            message.delete()

        context.chat_data["delete"] = [description_message]

        return ProductStates.DESCRIPTION

    @staticmethod
    def go_back(update: Update, context: CallbackContext):
        for message in context.chat_data["delete"]:
            message.delete()

        ProductCallbacks._product_list(update, context)

        return ProductStates.PRODUCTS
