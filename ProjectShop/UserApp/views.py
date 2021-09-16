from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.views import generic
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from UserApp.permissions import IsAdminBot
from UserApp.forms import LoginForm, RegisterForm


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'UserApp/login.html'


class RegisterView(SuccessMessageMixin, generic.CreateView):
    form_class = RegisterForm
    template_name = 'UserApp/register.html'
    success_url = reverse_lazy('login')
    success_message = "Congratulations! Your account has been created. You may sign in!"


class TemporalHomePageView(TemplateView):
    template_name = 'UserApp/home.html'


class BlacklistRefreshViewSet(viewsets.GenericViewSet):
    """
    A simple ViewSet for creating blacklist token from refresh token.
    """
    permission_classes = (IsAdminBot, IsAuthenticated)

    def create(self, request):
        try:
            refresh_token = RefreshToken(request.data.get('refresh'))
            refresh_token.blacklist()
        except TokenError as error:
            return Response(str(error), status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_200_OK)
