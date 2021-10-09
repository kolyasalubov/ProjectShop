from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.viewsets import ModelViewSet

from ProductApp.models import Review, Product, ProductCategory
from ProductApp.serializers import ReviewSerializer


class HomePageView(generic.ListView):
    # model = Product
    context_object_name = 'products'
    template_name = 'ProductApp/homepage.html'
    queryset = Product.objects.all()
    # paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = self.get_related_categories()
        products = self.get_related_products()
        context['categories'] = categories
        context['products'] = products
        return context

    def get_related_categories(self):
        queryset = ProductCategory.objects.all()
        paginator = Paginator(queryset, 20)
        page = self.request.GET.get('page')
        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            categories = paginator.page(1)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)
        return categories

    def get_related_products(self):
        queryset = Product.objects.all()
        paginator = Paginator(queryset, 12)
        page = self.request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return products


class CategoriesView(generic.ListView):
    model = ProductCategory
    context_object_name = 'categories'
    template_name = 'ProductApp/categories.html'
    paginate_by = 12


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
