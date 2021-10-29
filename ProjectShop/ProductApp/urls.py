# from ProductApp.router import product_router
from django.urls import path
from . import views
from ProductApp.views import  HomePageView, CategoriesView


urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('', HomePageView.as_view(), name='home'),
]

