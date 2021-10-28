# from ProductApp.router import product_router
from django.urls import path
from . import views
from ProductApp.views import ProductOverviewPageView, HomePageView, CategoriesView


urlpatterns = [
    path('overview/<int:product_id>', views.ProductOverviewPageView, name='product_overview'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('', HomePageView.as_view(), name='home'),
]

