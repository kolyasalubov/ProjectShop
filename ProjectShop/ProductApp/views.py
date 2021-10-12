from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.viewsets import ModelViewSet

from ProductApp.models import Review, Product, ProductCategory
from ProductApp.serializers import ReviewSerializer
from ProductApp.forms import SearchForm


class HomePageView(generic.ListView, generic.FormView):
    context_object_name = 'products'
    template_name = 'ProductApp/homepage.html'
    form_class = SearchForm
    queryset = Product.objects.all()
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.order_by('name')[:20]
        context['categories'] = categories
        return context


class CategoriesView(generic.ListView):
    model = ProductCategory
    context_object_name = 'categories'
    template_name = 'ProductApp/categories.html'
    paginate_by = 12


class SearchResultsListView(generic.ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'ProductApp/search_results.html'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(name__icontains=query, stock_quantity__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.order_by('name')[:20]
        context['categories'] = categories
        return context


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
