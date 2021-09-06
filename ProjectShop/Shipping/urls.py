from django.urls import path
from .views import *

urlpatterns = [
    path('add/', add_shipping_address),
    path('all/', all_shipping_addresses),
    path('<id>', detail_shipping_address),
    path('update/<id>', update_shipping_address),
    path('delete/<id>', delete_shipping_address),
]
