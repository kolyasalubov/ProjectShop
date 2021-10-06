from models import User
import phonenumbers
from pydantic.error_wrappers import ValidationError


a = User.get_user_by_phone_number('+380980589874')
print(a.content)


