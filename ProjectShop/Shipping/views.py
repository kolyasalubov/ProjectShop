from rest_framework import viewsets, renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from Shipping.models import ShippingModel

from Shipping.serializers import ShippingSerializer


class ShippingViewSet(viewsets.ModelViewSet):
    """
    A viewSet for Shipping model
    """
    queryset = ShippingModel.objects.all()
    serializer_class = ShippingSerializer
    http_method_names = ['post', 'get', 'patch', 'put']
