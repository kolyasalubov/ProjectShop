import factory
from faker import Faker

from UserApp.models import User


def fake_phone_number() -> str:
	fake = Faker('uk_UA')
	return fake.phone_number()


class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

	first_name = factory.Faker('first_name')
	last_name = factory.Faker('last_name')
	birth_date = factory.Faker('date_of_birth')
	phone_number = factory.LazyFunction(fake_phone_number)
	email = factory.Faker('email')
	password = factory.PostGenerationMethodCall('set_password', 'ValidPassword1@')