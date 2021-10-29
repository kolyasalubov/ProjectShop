from django.views import generic

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from django_filters.views import FilterView

from ProductApp.models import Review, Product, ProductCategory
from ProductApp.serializers import ReviewSerializer
from ProductApp.filters import ProductFilter

from ProductApp.models import (
    Product,
    ProductCategory,
    ProductSubcategory,
    ProductImage,
    ProductVideo,
    Review,
    Tag,
    Reply,
)
from ProductApp.serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    ProductSubcategorySerializer,
    ProductImageSerializer,
    ProductVideoSerializer,
    ReviewSerializer,
    TagSerializer,
    ReplySerializer,
)


class HomePageView(FilterView):
    filterset_class = ProductFilter
    template_name = 'ProductApp/homepage.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.order_by('name')[:20]
        context['categories'] = categories
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = 'product_detail'
    template_name = 'ProductApp/product_detail.html'


class CategoriesView(generic.ListView):
    model = ProductCategory
    context_object_name = 'categories'
    template_name = 'ProductApp/categories.html'
    paginate_by = 12


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


class ReviewViewSet(NestedViewSetMixin, ModelViewSet):
    """
    ViewSet to view and write reviews for specified in path product
    """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class ReplyViewSet(NestedViewSetMixin, ModelViewSet):
    """
    ViewSet to view and write reviews for specified in path product
    """

    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
