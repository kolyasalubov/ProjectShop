from models import User
from phonenumbers import PhoneNumber

a = User(first_name="oleasfsdfgh", last_name="olesdgdsgh", phone_number=PhoneNumber("+380500555555"), email="o1@o.com")
print(a.register())
print(str(a.phone_number))



