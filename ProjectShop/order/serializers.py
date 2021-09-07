from rest_framework import serializers

from order.models import Order


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for Order/Create and Order/Detail views"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Order
        fields = "__all__"

class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for Order/all view"""
    class Meta:
        model = Order
        fields = ("id","order_date", "payment_method", "user")

