from django.test import TestCase
from django.db.utils import IntegrityError

from Shipping.tests.factories import ShippingFactory

class ShippingTestCase(TestCase):
    """Implement some tests for Shipping model"""

    def setUp(self) -> None:
        self.shipping = ShippingFactory()

    def test_create(self):
        shipping = self.shipping
        self.assertIsNotNone(shipping)

    def test_user_exists(self):
        shipping = self.shipping
        self.assertTrue(shipping.user.exists())

    def test_city_str(self):
        shipping = self.shipping
        self.assertEqual(shipping.city, shipping.__str__())

    def test_region_str(self):
        shipping = self.shipping
        self.assertEqual(shipping.region, shipping.__str__())

    def test_country_str(self):
        shipping = self.shipping
        self.assertEqual(shipping.country, shipping.__str__())

    def test_postal_code_max(self):
        shipping = self.shipping
        self.assertLessEqual(len(str(shipping.postal_code)), 10)
