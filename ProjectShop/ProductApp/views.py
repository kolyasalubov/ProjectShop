from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from ProductApp.models import (
    Product,
    ProductCategory,
    ProductSubcategory,
    ProductImage,
    ProductVideo,
    Review,
    Tag,
)
from ProductApp.serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    ProductSubcategorySerializer,
    ProductImageSerializer,
    ProductVideoSerializer,
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


class ProductImageViewSet(ReadOnlyModelViewSet):
    """This is viewset for ProductMedia model"""

    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()


class ProductVideoViewSet(ReadOnlyModelViewSet):
    """This is viewset for ProductMedia model"""

    serializer_class = ProductVideoSerializer
    queryset = ProductVideo.objects.all()


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
