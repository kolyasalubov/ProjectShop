import factory
from faker import Faker
from UserApp.models import User
from UserApp.tests.custom_providers import CustomPhoneProvider


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
