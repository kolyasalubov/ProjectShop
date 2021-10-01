from rest_framework import routers

from order.views import OrderViewSet, OrderItemsViewSet
from ProductApp.views import ReviewViewSet

router = routers.DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register(r'product/(?P<product_id>\d+)/reviews', ReviewViewSet, basename="reviews")
router.register('orderitems', OrderItemsViewSet, basename='orderitems')
