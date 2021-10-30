from django.shortcuts import render, redirect
from django.views import generic, View

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

from ProductApp.forms import ReviewForm

from django.db.models import Q


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


def ProductOverviewPageView(request, product_id = 1):
    product__object = Product.get_product_by_id(product_id=product_id)
    product_media = ProductImage.get_media_by_product(product = product__object)
    product_media_video = ProductVideo.get_media_video_by_product(product = product__object)
    product_all = ProductImage.objects.filter(~Q(product_id=product_id))

    new_review = None
    reviews = Review.get_review_by_product(product = product__object)

    if request.method == 'POST':
        review_form = ReviewForm(user = request.user ,data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product__object
            new_review.save()

            return redirect('product_overview', product_id=product_id )
    else:
        review_form = ReviewForm()

    context = {
        'product_object' : product__object,
        'product_media' : product_media,
        'product_media_video' : product_media_video,
        'product_all' : product_all,

        'comments': reviews,
        'new_comment': new_review,
        'comment_form': review_form
    }

    return render(request, 'ProductApp/ProductOverviewPage.html', context)


# class ClassBasedProductOverviewView(View):
#
#     product__object = Product.get_product_by_id(product_id=product_id)
#     product_media = ProductImage.get_media_by_product(product=product__object)
#     product_media_video = ProductVideo.get_media_video_by_product(product=product__object)
#     product_all = ProductImage.objects.filter(~Q(product_id=product_id))
#
#     new_review = None
#     reviews = Review.get_review_by_product(product=product__object)
#
#     def post(self, request):
#         review_form = ReviewForm(user=request.user, data=request.POST)
#         if review_form.is_valid():
#             new_review = review_form.save(commit=False)
#             new_review.product = self.product__object
#             new_review.save()
#
#             return redirect('product_overview', product_id=self.product_id)
#
#         return render(request, 'ProductApp/ProductOverviewPage.html', {
#             'product_object': self.product__object,
#             'product_media': self.product_media,
#             'product_media_video': self.product_media_video,
#             'product_all': self.product_all,
#
#             'comments': self.reviews,
#             'new_comment': self.new_review,
#             'comment_form': review_form
#         })
#
#     def get(self, request):
#         review_form = ReviewForm()
#         return render(request, 'ProductApp/ProductOverviewPage.html', {
#             'product_object': self.product__object,
#             'product_media': self.product_media,
#             'product_media_video': self.product_media_video,
#             'product_all': self.product_all,
#
#             'comments': self.reviews,
#             'new_comment': self.new_review,
#             'comment_form': review_form
#         })

