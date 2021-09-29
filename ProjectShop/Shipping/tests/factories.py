import factory

from Shipping.models import ShippingModel
from UserApp.tests.factories import UserFactory


class ShippingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShippingModel

    user = factory.SubFactory(UserFactory)

    postal_code = factory.Faker('45678')
    country = factory.Faker('UA')
    region = factory.Faker('Lvivska oblast')
    city = factory.Faker('Lviv')
    post_office = factory.Faker('random_int', min=1, max=89)
