from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from order.models import Order
from order.serializers import OrderDetailSerializer
from order.serializers import OrderListSerializer


class OrderCreateView(generics.CreateAPIView):
    """View of page order/create."""
    serializer_class = OrderDetailSerializer


class OrderListView(generics.ListAPIView):
    """View page of the all orders.
    Only for authenticated admins."""
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Specific order detail view"""
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)

