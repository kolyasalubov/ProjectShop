from rest_framework import routers
from order.views import OrderViewSet

orderRouter = routers.DefaultRouter()
orderRouter.register('order', OrderViewSet, basename='order')
