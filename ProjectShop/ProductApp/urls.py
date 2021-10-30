from django.urls import path
from . import views
from ProductApp.views import HomePageView, CategoriesView, ProductDetailView, ProductOverviewPageView


urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('overview/<int:product_id>', views.ProductOverviewPageView, name='product_overview'),
    path('', HomePageView.as_view(), name='home'),
]
