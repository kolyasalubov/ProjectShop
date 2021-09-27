from rest_framework import serializers

from UserApp.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'birth_date', 'register_date', 'phone_number',
                  'email', 'role', 'is_active', ]
        read_only_fields = ('id', 'register_date', 'is_active', 'email')


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number']
        read_only_fields = ['id', 'phone_number']
