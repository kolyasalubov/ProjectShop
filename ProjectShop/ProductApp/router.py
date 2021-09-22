from rest_framework import routers

from ProductApp.views import ProductViewSet

product_router = routers.DefaultRouter()
product_router.register('product', ProductViewSet, basename='product')
