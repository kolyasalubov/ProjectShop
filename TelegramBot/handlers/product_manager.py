from client.models import Category
from handlers.general import create_keyboard


def propose_categories(update, context):
    """
    Callback function for message handler 'search products'. Returns to bot InlineKeyboard with first page of categories
    """
    categories = Category.get()
    print(categories)
    keyboard = create_keyboard(categories, 2)
    message = context.bot.send_message(chat_id=update.message.chat_id, text="Choose category:", reply_markup=keyboard)
    if context.chat_data['category_list']:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.chat_data['category_list'])
    context.chat_data['category_list'] = message.id


def turn_categories_page(update, context):
    """
    Callback function for CallbackQueryHandler with path for turning pages.
    """
    print(update)
