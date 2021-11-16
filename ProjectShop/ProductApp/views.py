from django_filters.views import FilterView
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

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
from ProductApp.filters import ProductFilter

from django.db.models import Q


class CategoryListMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.order_by('name')[:20]
        context['categories'] = categories
        return context


class HomePageView(CategoryListMixin, FilterView):
    filterset_class = ProductFilter
    template_name = "ProductApp/homepage.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.all().order_by("-stock_quantity")


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = "product_detail"
    template_name = "ProductApp/product_detail.html"


class CategoriesView(generic.ListView):
    model = ProductCategory
    context_object_name = "categories"
    template_name = "ProductApp/categories.html"
    paginate_by = 12


class CategoryDetailView(CategoryListMixin, generic.DetailView):
    model = ProductCategory
    context_object_name = "category_detail"
    template_name = "ProductApp/Products_by_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_related_products()
        context["products"] = products
        return context

    def get_related_products(self):
        queryset = Product.objects.filter(categories=self.object)
        ordered_queryset = queryset.order_by("-stock_quantity")
        paginator = Paginator(ordered_queryset, 12)
        try:
            page = self.request.GET.get("page")
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        products = paginator.get_page(page)
        return products


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


def ProductOverviewPageView(request, slug):
    product__object = Product.get_product_by_slug(slug = slug)
    product_media = ProductImage.get_media_by_product(product = product__object)
    product_media_video = ProductVideo.get_media_video_by_product(product = product__object)
    product_all = ProductImage.objects.filter(~Q(product = product__object))

    new_review = None
    reviews = Review.get_review_by_product(product = product__object)

    if request.method == 'POST':
        review_form = ReviewForm(user = request.user ,data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product__object
            new_review.save()

            return redirect('product_overview', slug=slug )
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




def category_detail_view(request):
    obj = Product.objects.get(id=1)
    # img = ProductMedia.objects.get(id=1)
    context = {
        "product": obj,
        # "product_img": img,
    }
    return render(request, "order/make_order.html", context)


def product_detail_view(request):
    obj = Product.objects.all()
    context = {
        "obj": obj
    }

    return render(request, "order/test_products.html", context)


def product_detail_view_new(request):
    obj = Product.objects.all()
    context = {
        "obj": obj
    }

    return render(request, "ProductApp/homepage.html", context)