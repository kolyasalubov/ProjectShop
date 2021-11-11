from django.urls import path
from . import views

from ProductApp.views import (
    HomePageView,
    CategoriesView,
    ProductDetailView,
    CategoryDetailView,
    ProductOverviewPageView,
    ProductsByTagGroupView,
    ProductJsonListView
)


urlpatterns = [
    path("categories/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path('bytag/', views.ProductsByTagGroupView, name='products_by_tag_group'),
    path('overview/<int:product_id>', views.ProductOverviewPageView, name='product_overview'),
    path('', HomePageView.as_view(), name='home'),
    # path('products-json/<int:num_products>/', ProductJsonListView.as_view(), name='products-json-view'),
]
