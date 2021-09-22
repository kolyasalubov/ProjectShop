from django.urls import path, include
from django.contrib import admin
from ProductApp.router import product_router

app_name = "ProductApp"
urlpatterns = product_router.urls
