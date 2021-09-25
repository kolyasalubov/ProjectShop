from rest_framework import viewsets

from order.models import OrderModel
from order.serializers import OrderDetailSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """This is viewset for order model"""
    queryset = OrderModel.objects.all()
    serializer_class = OrderDetailSerializer
