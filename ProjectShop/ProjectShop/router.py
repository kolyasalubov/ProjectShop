from rest_framework_extensions.routers import ExtendedSimpleRouter

from ProductApp.views import (
    ProductViewSet,
    ReviewViewSet,
    TagViewSet,
    ProductImageViewSet,
    ProductVideoViewSet,
    ProductCategoryViewSet,
    ProductSubcategoryViewSet,
)
from Shipping.views import ShippingViewSet
from UserApp.views import UserViewSet
from order.views import OrderViewSet, OrderItemsViewSet
from UserApp.views import UserViewSet, WishListViewSet


router = ExtendedSimpleRouter()
router.register(r"order", OrderViewSet, basename="order")
router.register(r"orderitems", OrderItemsViewSet, basename="orderitems")
router.register(r"product", ProductViewSet, basename="product") \
    .register(r'reviews', ReviewViewSet, basename='product_reviews', parents_query_lookups=["product"])
router.register(r"categories", ProductCategoryViewSet, basename="categories")
router.register(r"subcategories", ProductSubcategoryViewSet, basename="subcategories")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"product_image", ProductImageViewSet, basename="product_image")
router.register(r"product_video", ProductVideoViewSet, basename="product_video")
router.register(r"shipping", ShippingViewSet, basename="shipping")
router.register(r"user", UserViewSet, basename="user")\
    .register(r'wishlist', WishListViewSet, basename='user_wishlist', parents_query_lookups=['id'])
