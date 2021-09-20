from rest_framework import serializers

from ProductApp.serializers import ProductSerializer
from UserApp.models import User


class WishListSerializer(serializers.ModelSerializer):
    wishlist = ProductSerializer(many=True, read_only=True)

    class Meta:
        model: User
        fields = ['wishlist']
        read_only_fields = ['wishlist']
