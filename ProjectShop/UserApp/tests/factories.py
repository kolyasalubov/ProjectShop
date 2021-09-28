import factory
from UserApp.models import User
from faker import Faker
import phonenumbers
from faker.providers.phone_number.uk_UA import Provider


class CustomPhoneProvider(Provider):
    def phone_number(self):
        '''Creation of our own phone_number provider'''
        while True:
            phone_number = self.numerify(self.random_element(self.formats))
            parsed_number = phonenumbers.parse(phone_number, 'UA')
            if phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(
                    parsed_number,
                    phonenumbers.PhoneNumberFormat.E164
                )

fake = Faker()
fake.add_provider(CustomPhoneProvider)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    birth_date = factory.Faker('date_of_birth')
    phone_number = factory.LazyFunction(lambda : fake.phone_number())
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'ValidPassword1@')