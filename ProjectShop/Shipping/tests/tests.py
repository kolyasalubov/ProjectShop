from django.test import TestCase
from django.db.utils import IntegrityError

from Shipping.tests.factories import *

class ShippingTestCase(TestCase):
	def setUp(self) -> None:
		pass

    def test_create(self):
        shipping = ShippingFactory()
        self.assertIsNotNone(shipping)

        





