from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from UserApp.permissions import IsBot
from UserApp.serializers import RegisterUserSerializer


class UserCreate(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated, IsBot)
    serializer_class = RegisterUserSerializer
