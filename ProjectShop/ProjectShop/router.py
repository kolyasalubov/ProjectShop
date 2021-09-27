from rest_framework import routers
from order.views import OrderViewSet

router = routers.DefaultRouter()
router.register('order', OrderViewSet, basename='order')
