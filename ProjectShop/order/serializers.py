from rest_framework import serializers
from order.models import OrderModel


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for Order view"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = OrderModel
        fields = "__all__"
