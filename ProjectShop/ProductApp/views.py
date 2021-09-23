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
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()


class ProductSubcategoryViewSet(ModelViewSet):
    serializer_class = ProductSubcategorySerializer
    queryset = ProductSubcategory.objects.all()


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class ProductMediaViewSet(ModelViewSet):
    serializer_class = ProductMediaSerializer
    queryset = ProductMedia.objects.all()
