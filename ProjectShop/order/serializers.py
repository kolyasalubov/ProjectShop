from rest_framework import serializers
from order.models import Order


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

