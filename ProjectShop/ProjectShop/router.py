from rest_framework import routers

from order.views import OrderViewSet, OrderItemsViewSet
from ProductApp.views import ProductViewSet, ReviewViewSet
from UserApp.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register('orderitems', OrderItemsViewSet, basename='orderitems')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'product/(?P<product_id>\d+)/reviews', ReviewViewSet, basename="reviews")
router.register(r'user', UserViewSet, basename='userviewset')
