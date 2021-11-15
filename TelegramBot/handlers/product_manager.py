from enum import Enum

from callbacks.callbacks import (
    MessageCallback,
    EditMessageCallback,
    ReturnMessageCallback,
)
from callbacks.data_loaders import (
    FirstPageModelLoader,
    TurnPageModelLoader,
    CallbackDataLoader,
    UpdateTextLoader,
    ModelInstanceLoader,
)
from callbacks.menu_builders import (
    InlineKeyboardBuilder,
    PaginatedInlineKeyboardBuilder,
    MessageMenuBuilder,
)
from callbacks.message_builders import (
    MessageBuilder,
    MessageKeyboardEditor,
    PageMessageGroupBuilder,
    AlbumBuilder,
    PhotoMessageRebuilder,
)
from callbacks.message_history_managers import MessageHistoryManager
from callbacks.schemas import BaseSchema, PageSchema
from client.models import Category, Product


class ProductStates(Enum):
    SEARCH, CATEGORY, NAME, PRODUCTS, DESCRIPTION = range(5)


class ProposeTypeSearch(MessageCallback):
    name = "propose_search"
    delete = "update"
    schema = BaseSchema("propose_search_type")
    menu = InlineKeyboardBuilder
    message = MessageBuilder
    state = ProductStates.SEARCH


class ProposeCategories(MessageCallback):
    name = "propose_categories"
    delete = "propose_search"
    load = FirstPageModelLoader(Category)
    schema = BaseSchema("propose_categories")
    menu = PaginatedInlineKeyboardBuilder
    message = MessageBuilder
    state = ProductStates.CATEGORY


class CategoryTurnPage(EditMessageCallback):
    edit = "propose_categories"
    load = TurnPageModelLoader(Category, CallbackDataLoader())
    schema = BaseSchema("propose_categories")
    menu = PaginatedInlineKeyboardBuilder
    message = MessageKeyboardEditor


class AskForQuery(MessageCallback):
    name = "ask_query"
    delete = "propose_search"
    schema = BaseSchema("ask_query")
    message = MessageBuilder
    state = ProductStates.NAME


class SearchByQuery(MessageCallback):
    name = "product_list"
    delete = ["ask_query", "update"]
    load = FirstPageModelLoader(Product, UpdateTextLoader("query"))
    schema = PageSchema("product_list", key="product")
    menu = MessageMenuBuilder
    message = PageMessageGroupBuilder
    state = ProductStates.PRODUCTS


class SearchByCategory(MessageCallback):
    name = "product_list"
    delete = "propose_categories"
    load = FirstPageModelLoader(Product, CallbackDataLoader())
    schema = PageSchema("product_list", key="product")
    menu = MessageMenuBuilder
    message = PageMessageGroupBuilder
    state = ProductStates.PRODUCTS


class TurnProductPage(MessageCallback):
    name = "product_list"
    delete = "product_list"
    load = TurnPageModelLoader(Product, CallbackDataLoader())
    schema = PageSchema("product_list", key="product")
    menu = MessageMenuBuilder
    message = PageMessageGroupBuilder


class ProductDescription(MessageCallback):
    name = "product_description"
    delete = "product_list"
    history_manager = MessageHistoryManager(save_in_history=True)
    load = ModelInstanceLoader(Product, CallbackDataLoader(alias="product"))
    schema = BaseSchema("product_description")
    menu = [None, InlineKeyboardBuilder]
    message = [AlbumBuilder, MessageBuilder]
    state = ProductStates.DESCRIPTION


class ProductDescriptionBack(ReturnMessageCallback):
    name = "product_list"
    delete = "product_description"
    return_message = "product_list"
    message = PhotoMessageRebuilder
    state = ProductStates.PRODUCTS
