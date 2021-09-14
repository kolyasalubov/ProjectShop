from django.urls import path

from Shipping.views import AddShippingAddress, AllShippingAddresses, DetailShippingAddress
from Shipping.views import UpdateShippingAddress, DeleteShippingAddress

urlpatterns = [
    path('add/', AddShippingAddress.as_view(), name="add_address"),
    path('all/', AllShippingAddresses.as_view(), name="all_addresses"),
    path('<pk>/', DetailShippingAddress.as_view(), name="detail_address"),
    path('update/<pk>/', UpdateShippingAddress.as_view(), name="update_address"),
    path('delete/<pk>/', DeleteShippingAddress.as_view(), name="delete_address"),
]
