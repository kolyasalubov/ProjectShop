from django.shortcuts import render
from rest_framework import generics
from order.serializers import OrderDetailSerializer
from order.models import Order
from order.serializers import OrderListSerializer


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderDetailSerializer

class OrderListView(generics.CreateAPIView):
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()