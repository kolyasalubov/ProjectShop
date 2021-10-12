from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet 
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_extensions.mixins import NestedViewSetMixin

from ProductApp.models import Product, ProductCategory, ProductSubcategory, ProductMedia, Review, Tag
from ProductApp.serializers import (ProductSerializer, ProductCategorySerializer,
                                    ProductSubcategorySerializer, ProductMediaSerializer,
                                    ReviewSerializer, TagSerializer)


class ProductViewSet(ReadOnlyModelViewSet):
    """This is viewset for Product model"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCategoryViewSet(ReadOnlyModelViewSet):
    """This is viewset for ProductCategory model"""
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()


class ProductSubcategoryViewSet(ReadOnlyModelViewSet):
    """This is viewset for ProductSubcategory model"""
    serializer_class = ProductSubcategorySerializer
    queryset = ProductSubcategory.objects.all()


class TagViewSet(ReadOnlyModelViewSet):
    """This is viewset for Tag model"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class ProductMediaViewSet(ReadOnlyModelViewSet):
    """This is viewset for ProductMedia model"""
    serializer_class = ProductMediaSerializer
    queryset = ProductMedia.objects.all()


class ReviewViewSet(NestedViewSetMixin, ModelViewSet):
    """
    ViewSet to view and write reviews for specified in path product
    """
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

# def perform_create(self, serializer):
#     product_id = self.kwargs.get('product_id')
#     serializer.save(product=Product.objects.get(pk=product_id))
