import factory
import random

from WishList.models import WishList
from UserApp.tests.factories import UserFactory
from ProductApp.tests.factories import ProductFactory


class WishListFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = WishList

	user = factory.SubFactory(UserFactory)

	@factory.post_generation
	def products(self, create, extracted, **kwargs):
		products = extracted if extracted is not None else ProductFactory.create_batch(random.randint(1, 5))
		for product in products:
			self.products.add(product)
