from django.urls import path

from ProductApp.views import HomePageView, CategoriesView, ProductDetailView, ProductJsonListView


urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('', HomePageView.as_view(), name='home'),
    path('products-json/<int:num_products>/', ProductJsonListView.as_view(), name='products-json-view'),
]
