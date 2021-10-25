import django_filters

from ProductApp.models import Product


class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
        }
