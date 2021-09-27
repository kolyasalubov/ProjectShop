from rest_framework import viewsets, renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from order.models import Order
from order.models import OrderItems

from order.serializers import OrderDetailSerializer, OrderItemsSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """This is viewset for order model"""
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    http_method_names = ['post', 'get', 'patch', 'put']

class OrderItemsViewSet(viewsets.ReadOnlyModelViewSet):
    """This is viewset for order items model"""
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer