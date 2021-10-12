import factory
import datetime

from order.models import OrderModel, OrderItemsModel
from UserApp.tests.factories import UserFactory
from Shipping.tests.factories import ShippingFactory


# from ProductApp.tests.factories import ProductFactory


class OrderModelFactory(factory.django.DjangoModelFactory):
    """Implement factory for the order model
    using faker - a package that generates fake data for our tests"""

    class Meta:
        model = OrderModel

    user = factory.SubFactory(UserFactory)
    shippingAddress_id = factory.SubFactory(ShippingFactory)

    order_date = factory.Faker(datetime.datetime(2021, 9, 21, 11, 54, 40))
    payment_method = factory.Faker('random_int', min=0, max=1)
    shipping_status = factory.Faker('random_int', min=0, max=3)
    payment_status = factory.Faker('random_int', min=0, max=1)


class OrderItemsModelFactory(factory.django.DjangoModelFactory):
    """Implement factory for the order items model
    using faker - a package that generates fake data for our tests"""

    class Meta:
        model = OrderItemsModel

    order = factory.SubFactory(OrderModelFactory)
    # product = factory.SubFactory(ProductFactory)

    order_items_quantity = factory.Faker('random_int', min=1, max=100)
