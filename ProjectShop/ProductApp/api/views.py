from rest_framework import viewsets

from ProductApp.models import Product
from ProductApp.api.serializers import ProductReviewSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """This is viewset for reply model"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'product'
