from django.urls import path

from ProductApp.views import HomePageView, CategoriesView, ProductDetailView


urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('', HomePageView.as_view(), name='home'),
]
