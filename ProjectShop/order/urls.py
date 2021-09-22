from django.urls import path, include
from django.contrib import admin
from order.router import router

app_name = "order"

urlpatterns = router.urls
