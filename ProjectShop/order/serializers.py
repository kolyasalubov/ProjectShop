from rest_framework import serializers

from order.models import Order


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for Order view"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Order
        fields = "__all__"
