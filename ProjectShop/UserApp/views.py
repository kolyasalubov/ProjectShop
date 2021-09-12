from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from UserApp.permissions import IsBot
from UserApp.serializers import RegisterUserSerializer


class UserCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsBot)
    serializer_class = RegisterUserSerializer


class BlacklistRefreshView(APIView):

    def post(self, request):
        try:
            refresh_token = RefreshToken(request.data.get('refresh'))
            refresh_token.blacklist()
        except TokenError as error:
            return Response(str(error), status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_200_OK)
