from django.test import TestCase

from WishList.tests.factories import WishListFactory
from ProductApp.tests.factories import ProductFactory


class WishListTestCase(TestCase):
	def setUp(self) -> None:
		pass

	def test_create(self):
		wishlist = WishListFactory()
		self.assertIsNotNone(wishlist)

	def test_add_product(self):
		wishlist = WishListFactory()
		product_count = wishlist.products.all().count()
		product = ProductFactory()
		wishlist.products.add(product)
		self.assertEqual(wishlist.products.all().count(), product_count + 1)
