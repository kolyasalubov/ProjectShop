from rest_framework import routers

from ProductApp.views import ReviewViewSet
from order.views import OrderViewSet
from UserApp.views import UserViewSet

router = routers.DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register(r'product/(?P<product_id>\d+)/reviews', ReviewViewSet, basename="reviews")
router.register(r'user', UserViewSet, basename='userviewset')
