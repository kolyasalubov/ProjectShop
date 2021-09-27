from rest_framework import routers
from order.views import OrderViewSet, OrderItemsViewSet

router = routers.DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('orderitems', OrderItemsViewSet, basename='orderitems')
