from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

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
