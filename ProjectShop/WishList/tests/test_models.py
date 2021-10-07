from django.test import TestCase

from ProductApp.tests.factories import ProductFactory
from WishList.tests.factories import WishListFactory


class WishListTestCase(TestCase):
    """Test Case for WishList model"""

    def setUp(self) -> None:
        self.wishlist = WishListFactory()

    def test_create(self):
        wishlist = self.wishlist
        self.assertIsNotNone(wishlist)

    def test_add_product(self):
        wishlist = self.wishlist
        product_count = wishlist.products.all().count()
        product = ProductFactory()
        wishlist.products.add(product)
        wishlist.save()
        self.assertEqual(wishlist.products.all().count(), product_count + 1)
