from rest_framework import serializers

from Shipping.models import ShippingModel


class ShippingSerializer(serializers.ModelSerializer):
    """A serializer for Shipping view"""

    class Meta:
        model = ShippingModel
        fields = "__all__"
