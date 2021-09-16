from rest_framework import serializers
from order.models import Order


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id","order_date", "payment_method", "user")

