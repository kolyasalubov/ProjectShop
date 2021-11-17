import factory

from Shipping.models import ShippingModel
from UserApp.tests.factories import UserFactory


class ShippingFactory(factory.django.DjangoModelFactory):
    """Implement factory for the Shipping model
        using faker - a package that generates fake data for our tests"""

    class Meta:
        model = ShippingModel

    user = factory.SubFactory(UserFactory)

    postal_code = factory.Faker("random_int", min=79007, max=79068)    # generate one of all postal codes of the Lviv
    country = "UA"
    region = "Lvivska oblast"
    city = "Lviv"
    post_office = factory.Faker("random_int", min=1, max=89)
