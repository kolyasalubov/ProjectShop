from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from ProductApp.models import Review, Product
from ProductApp.serializers import ReviewSerializer


class ReviewViewSet(ModelViewSet):
    """
    ViewSet to view and write reviews for specified in path product
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        queryset_list = Review.objects.filter(product=product_id)
        return queryset_list

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        serializer.save(product=Product.objects.get(pk=product_id))
