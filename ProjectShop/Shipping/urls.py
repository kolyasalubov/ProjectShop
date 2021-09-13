from django.urls import path
from .views import *

urlpatterns = [
    path('add/', AddShippingAddress.as_view()),
    path('all/', AllShippingAddresses.as_view()),
    path('<pk>/', DetailShippingAddress.as_view()),
    path('update/<pk>/', UpdateShippingAddress.as_view()),
    path('delete/<pk>/', DeleteShippingAddress.as_view()),
]
