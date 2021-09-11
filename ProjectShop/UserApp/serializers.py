from rest_framework import serializers, status
from rest_framework.response import Response
import django.contrib.auth.password_validation as validators


from UserApp.models import User


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_password(value):
        validators.validate_password(value)
        return value

    def create(self, validated_data, *args, **kwargs):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance



