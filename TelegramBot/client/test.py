from models import User
from models import bot_client
import phonenumbers
from pydantic.error_wrappers import ValidationError


# a = User.get_user_by_phone_number('+380666666666', 'fg')
# print(a)

b = User(telegram_id='lkjk',id=10,first_name='first_name', last_name='last_name', phone_number='+380505555555', email='mail@email.com')

b.first_name = 'alkfklsd'