from rest_framework.routers import DefaultRouter

from ProductApp.views import ProductViewSet

app_name = 'product_app'

productRouter = DefaultRouter()
productRouter.register(r'product', ProductViewSet, basename='product')
"""
productRouter.register(r'product/(?P<product>\d+)/categories', ProductCategoryViewSet, basename="categories")
productRouter.register(r'product/(?P<product>\d+)/subcategories', ProductSubcategoryViewSet, basename="subcategories")
productRouter.register(r'product/(?P<product>\d+)/tags', TagViewSet, basename="tags")
productRouter.register(r'product/(?P<product>\d+)/media', ProductMediaViewSet, basename="media")
"""
# uncomment to add categories, subcategories, tags and media
