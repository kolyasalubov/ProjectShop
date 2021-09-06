from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from UserApp.serializers import UserSerializer, UserListSerializer
from UserApp.models import User


class UserRestView(generics.RetrieveAPIView):
    """View of one user model object"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'
    permission_classes = {IsAuthenticated, IsAdminUser}


class UserRestListView(generics.ListAPIView):
    """View list of all user model objects"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'
    permission_classes = {IsAuthenticated, IsAdminUser}

