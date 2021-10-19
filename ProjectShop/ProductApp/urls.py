# from ProductApp.router import product_router
from django.urls import path
from . import views
from ProductApp.views import ProductOverviewPageView

#app_name = "ProductApp"


urlpatterns = [
    path('overview/<int:product_id>', views.ProductOverviewPageView, name='product_overview'),
]
