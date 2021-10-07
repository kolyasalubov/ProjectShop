from rest_framework import routers

from ProductApp.views import (
    ProductViewSet,
    ReviewViewSet,
    TagViewSet,
    ProductMediaViewSet,
    ProductCategoryViewSet,
    ProductSubcategoryViewSet
)
from Shipping.views import ShippingViewSet
from UserApp.views import UserViewSet
from order.views import OrderViewSet, OrderItemsViewSet

router = routers.DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register(r'orderitems', OrderItemsViewSet, basename='orderitems')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'categories', ProductCategoryViewSet, basename='categories')
router.register(r'subcategories', ProductSubcategoryViewSet, basename='subcategories')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'product_media', ProductMediaViewSet, basename='product_media')
router.register(r'product/(?P<product_id>\d+)/reviews', ReviewViewSet, basename="reviews")
router.register(r'shipping', ShippingViewSet, basename='shipping')
router.register(r'user', UserViewSet, basename='user')
