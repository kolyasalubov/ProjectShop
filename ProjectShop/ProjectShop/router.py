from rest_framework import routers

from order.views import OrderViewSet
from ProductApp.views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register(r'product', ProductViewSet, basename='product')
