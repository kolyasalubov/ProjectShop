from rest_framework import viewsets

from order.models import Order, OrderItems
from order.serializers import OrderDetailSerializer, OrderItemsSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """This is viewset for order model"""

    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    http_method_names = ["post", "get", "patch", "put"]


class OrderItemsViewSet(viewsets.ModelViewSet):
    """This is viewset for order items model"""

    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    http_method_names = ["post", "get", "patch", "put"]
