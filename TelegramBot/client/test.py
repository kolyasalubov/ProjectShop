from models import User
import phonenumbers
from pydantic.error_wrappers import ValidationError
# try:
#     a = User(first_name="oleassadfsdfgh", last_name="oleshhhhhhhhgdsgh", phone_number=
#     "+38050055555535436456w3455t", email="o1@o.com")
# except ValidationError as s:
#     print(s.errors())

# print(a.register())
# print(str(a.phone_number))


a = "+380980589874"
my_number = phonenumbers.parse(a)
print(my_number)
print(phonenumbers.is_possible_number(my_number))
print(phonenumbers.is_valid_number(my_number))
print(phonenumbers.normalize_digits_only(my_number))


