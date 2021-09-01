from django.urls import path, include
from django.contrib import admin
from order.views import *

app_name = "order"
urlpatterns = [
    path('create/', OrderCreateView.as_view()),
    path('all/', OrderListView.as_view()),
    path('order/detail/<int:pk>/', OrderDetailView.as_view()),

]