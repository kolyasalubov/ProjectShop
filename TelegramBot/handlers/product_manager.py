from client.models import Category
from handlers.general import create_keyboard


def propose_categories(update, context):
    categories = Category.get()
    keyboard = create_keyboard(categories, 2)
    context.bot.send_message(chat_id=update.message.chat_id, text="Choose category:", reply_marku=keyboard)


