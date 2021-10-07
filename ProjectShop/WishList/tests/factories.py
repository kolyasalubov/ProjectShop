import random

import factory

from ProductApp.tests.factories import ProductFactory
from UserApp.tests.factories import UserFactory
from WishList.models import WishList


class WishListFactory(factory.django.DjangoModelFactory):
    """Factory for WishList model"""

    class Meta:
        model = WishList

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        products = extracted if extracted is not None \
            else ProductFactory.create_batch(random.randint(1, 5))
        for product in products:
            self.products.add(product)
