from rest_framework import routers

from ProductApp.views import ReviewViewSet

app_name = 'product_app'

productRouter = routers.DefaultRouter()
productRouter.register(r'(?P<product_id>\d+)/reviews', ReviewViewSet, basename="reviews")
