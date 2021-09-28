from rest_framework import routers

from order.views import OrderViewSet
from Shipping.views import ShippingViewSet

router = routers.DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('shipping', ShippingViewSet, basename='shipping')
