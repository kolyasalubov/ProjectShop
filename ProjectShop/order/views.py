from rest_framework import viewsets

from order.models import Order
from order.models import OrderItems

from order.serializers import OrderDetailSerializer, OrderItemsSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """This is viewset for order model"""
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

class OrderItemsViewSet(viewsets.ReadOnlyModelViewSet):
    """This is viewset for order items model"""
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer