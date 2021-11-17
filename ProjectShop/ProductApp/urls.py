from django.urls import path

from ProductApp.views import (
    HomePageView,
    CategoriesView,
    ProductDetailView,
    CategoryDetailView,
)


urlpatterns = [
    path("categories/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("", HomePageView.as_view(), name="home"),
]
