from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from ProductApp.models import Product, ProductCategory, ProductSubcategory, ProductMedia, Review, Tag
from ProductApp.serializers import ProductSerializer, ProductCategorySerializer, ProductSubcategorySerializer
from ProductApp.serializers import ProductMediaSerializer, ReviewSerializer, TagSerializer


class ProductViewSet(ModelViewSet):
    """This is viewset for Product model"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCategoryViewSet(ModelViewSet):
    """This is viewset for ProductCategory model"""
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()


class ProductSubcategoryViewSet(ModelViewSet):
    """This is viewset for ProductSubcategory model"""
    serializer_class = ProductSubcategorySerializer
    queryset = ProductSubcategory.objects.all()


class TagViewSet(ModelViewSet):
    """This is viewset for Tag model"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class ProductMediaViewSet(ModelViewSet):
    """This is viewset for ProductMedia model"""
    serializer_class = ProductMediaSerializer
    queryset = ProductMedia.objects.all()
