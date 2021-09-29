from django.test import TestCase
from django.db.utils import IntegrityError

from order.tests.factories import *


class OrderModelTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_name(self):
        Order = OrderModelFactory()
        self.assertIsNotNone(Order)

class OrderItemsModelTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_name(self):
        OrderItems = OrderItemsModelFactory()
        self.assertIsNotNone(OrderItems)