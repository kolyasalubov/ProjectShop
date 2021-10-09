from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.viewsets import ModelViewSet

from ProductApp.models import Review, Product, ProductCategory
from ProductApp.serializers import ReviewSerializer


class HomePageView(generic.ListView):
    context_object_name = 'products'
    template_name = 'ProductApp/homepage.html'
    queryset = Product.objects.all()
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = self.get_related_categories()
        context['categories'] = categories
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
