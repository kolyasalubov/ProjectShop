from rest_framework import viewsets

from order.models import Product
from ProductApp.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """This is viewset for Product model"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

