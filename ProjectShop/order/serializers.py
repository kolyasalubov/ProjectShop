from rest_framework import serializers
from order.models import Order
from order.models import OrderItems


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for Order Detail view"""
    class Meta:
        model = Order
        fields = "__all__"

class OrderItemsSerializer(serializers.ModelSerializer):
    """Serializer for OrderItems view"""
    class Meta:
        model = OrderItems
        fields = "__all__"
