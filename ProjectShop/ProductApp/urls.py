# from ProductApp.router import product_router
from django.urls import path

from ProductApp.views import ProductsView

app_name = "ProductApp"

urlpatterns = [
    path("", ProductsView.as_view(), name="products"),
]
