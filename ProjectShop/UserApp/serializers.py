from rest_framework import serializers

from UserApp.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'register_date', 'phone_number',
                  'email', 'role', 'is_active', 'telegram_id']
        read_only_fields = ('id', 'register_date', 'is_active', 'role')


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

