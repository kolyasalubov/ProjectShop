from rest_framework import serializers
from order.models import Order, OrderItems


class OrderItemsSerializer(serializers.ModelSerializer):
    """Serializer for OrderItems view"""

    class Meta:
        model = OrderItems
        fields = ('product',
                  'order_items_quantity')


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for Order Detail view"""
    order_items = OrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id',
                  'order_date',
                  'shipping_status',
                  'payment_method',
                  'shippingAddress_id',
                  'payment_status', 'order_items')
