from rest_framework_extensions.routers import ExtendedSimpleRouter

from order.views import OrderViewSet, OrderItemsViewSet
from ProductApp.views import (ProductViewSet, TagViewSet, ProductMediaViewSet,
							  ProductCategoryViewSet, ProductSubcategoryViewSet, ReviewViewSet)
from Shipping.views import ShippingViewSet
from UserApp.views import UserViewSet

router = ExtendedSimpleRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register(r'orderitems', OrderItemsViewSet, basename='orderitems')
router.register(r'product', ProductViewSet, basename='product') \
	.register(r'reviews', ReviewViewSet, basename='product_reviews', parents_query_lookups=["product"])
router.register(r'categories', ProductCategoryViewSet, basename='categories')
router.register(r'subcategories', ProductSubcategoryViewSet, basename='subcategories')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'product_media', ProductMediaViewSet, basename='product_media')
router.register(r'shipping', ShippingViewSet, basename='shipping')
router.register(r'user', UserViewSet, basename='user')
