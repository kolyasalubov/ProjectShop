from rest_framework import viewsets

from Shipping.models import ShippingModel
from Shipping.serializers import ShippingSerializer


class ShippingViewSet(viewsets.ModelViewSet):
    """
    A viewSet for Shipping model
    """
    queryset = ShippingModel.objects.all()
    serializer_class = ShippingSerializer
    http_method_names = ['post', 'get', 'patch', 'put']
