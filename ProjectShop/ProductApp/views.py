from django.views import generic

from rest_framework.viewsets import ModelViewSet

from ProductApp.models import Review, Product, ProductCategory
from ProductApp.serializers import ReviewSerializer


class HomePageView(generic.ListView):
    context_object_name = 'categories'
    template_name = 'ProductApp/homepage.html'
    queryset = ProductCategory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
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
