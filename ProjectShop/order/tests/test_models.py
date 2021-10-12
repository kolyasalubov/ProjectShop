from django.test import TestCase
from django.db.utils import IntegrityError

from order.tests.factories import OrderModelFactory, OrderItemsModelFactory


class OrderModelTestCase(TestCase):
    """Implement some tests for Order model"""

    def setUp(self) -> None:
        self.Order = OrderModelFactory()

    def test_name(self):
        Order = self.Order
        self.assertIsNotNone(Order)

    def test_user_exists(self):
        Order = self.Order
        self.assertTrue(Order.user.exists())

    def test_shippingAddress_id_exists(self):
        Order = self.Order
        self.assertTrue(Order.shippingAddress_id.exists())

    def test_payment_method_max(self):
        Order = self.Order
        self.assertLessEqual(Order.payment_method, 1)

    def test_shipping_status_max(self):
        Order = self.Order
        self.assertLessEqual(Order.shipping_status, 3)


class OrderItemsModelTestCase(TestCase):
    """Implement some tests for OrderItems model"""

    def setUp(self) -> None:
        self.OrderItems = OrderItemsModelFactory()

    def test_name(self):
        OrderItems = self.OrderItems
        self.assertIsNotNone(OrderItems)

    def test_order_exists(self):
        OrderItems = self.OrderItems
        self.assertTrue(OrderItems.order.exists())

    def test_order_items_quantity_max(self):
        OrderItems = self.OrderItems
        self.assertLess(OrderItems.order_items_quantity, 101)
