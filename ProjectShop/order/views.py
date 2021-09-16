from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from UserApp.permissions import IsAdminBot
from order.serializers import OrderDetailSerializer
from order.models import Order
from order.serializers import OrderListSerializer


class OrderCreateView(generics.CreateAPIView):
    permission_classes = (IsAdminBot, IsAuthenticated)
    serializer_class = OrderDetailSerializer


class OrderListView(generics.ListAPIView):
    permission_classes = (IsAdminBot, IsAuthenticated)
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminBot, IsAuthenticated)
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
