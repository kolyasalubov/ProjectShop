from rest_framework import serializers

from UserApp.models import User
from ProductApp.serializers import ProductSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer that we use to serialize fields of model.
    """
    
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "birth_date",
            "register_date",
            "phone_number",
            "email",
            "role",
            "is_active",
            "telegram_id",
        ]
        read_only_fields = ("id", "register_date", "is_active", "role")


class UserSerializerForPatch(serializers.ModelSerializer):
    """
    Serializer that we use to serialize fields of model which we can change in PATCH.
    """

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'birth_date']


class UserWishListSerializer(serializers.ModelSerializer):
    """
    Serializer that we use to serialize wishlist.
    """
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'wishlist', 'products']
        depth = 2
