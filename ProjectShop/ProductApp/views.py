from django.shortcuts import render

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from ProductApp.models import (
    Product,
    ProductCategory,
    ProductSubcategory,
    ProductMedia,
    Review,
    Tag,
)
from ProductApp.serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    ProductSubcategorySerializer,
    ProductMediaSerializer,
    ReviewSerializer,
    TagSerializer,
)


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


class ReviewViewSet(ModelViewSet):
    """
    ViewSet to view and write reviews for specified in path product
    """

    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        queryset_list = Review.objects.filter(product=product_id)
        return queryset_list

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_id")
        serializer.save(product=Product.objects.get(pk=product_id))


def category_detail_view(request):
    obj = Product.objects.get(id=1)
    img = ProductMedia.objects.get(id=1)
    context = {
        "product": obj,
        "product_img": img,
    }
    return render(request, "order/make_order.html", context)


def product_detail_view(request):
    obj = Product.objects.all()
    context = {
        "obj": obj
    }

    return render(request, "order/test_products.html", context)
