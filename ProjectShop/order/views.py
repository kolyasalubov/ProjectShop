from rest_framework import viewsets

from order.models import Order
from order.serializers import OrderDetailSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """This is viewset for order model"""
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

