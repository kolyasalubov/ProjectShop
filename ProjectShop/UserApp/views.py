from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views, get_user_model
from django.views import generic
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from braces.views import AnonymousRequiredMixin
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from UserApp.permissions import IsAdminBot
from UserApp.forms import LoginForm, RegisterForm, EditForm
from UserApp.serializers import UserSerializer, UserIdSerializer
from UserApp.models import User


class LoginView(AnonymousRequiredMixin, auth_views.LoginView):
    form_class = LoginForm
    template_name = 'UserApp/login.html'


class RegisterView(AnonymousRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = RegisterForm
    template_name = 'UserApp/register.html'
    success_url = reverse_lazy('login')
    success_message = _("Congratulations! Your account has been created. You may sign in!")


class LogoutView(auth_views.LogoutView):
    template_name = 'UserApp/logout.html'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'UserApp/password_reset.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'UserApp/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'UserApp/password_reset_confirm.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'UserApp/password_reset_complete.html'


class TemporalHomePageView(TemplateView):
    template_name = 'UserApp/home.html'


class CustomUpdateView(generic.edit.SingleObjectTemplateResponseMixin,
                       generic.edit.ModelFormMixin,
                       generic.edit.ProcessFormView):

    def get(self, request, *args, **kwargs):
        self.object = request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = request.user
        return super().post(request, *args, **kwargs)


class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, CustomUpdateView):
    form_class = EditForm
    model = get_user_model
    template_name = 'UserApp/profile.html'
    success_url = reverse_lazy('profile')
    success_message = _("Your account has been updated!")


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


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        user = User.objects.filter(phone_number=request.data.get('phone_number'))
        if not user:
            return Response(data={'message': 'We haven\'t user with such phone number.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserIdSerializer(user, many=True)
        return Response(serializer.data)

    def patch(self, request):
        user = User.objects.get(phone_number=request.data.get('phone_number'))
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'We haven\'t user with such phone number.'})
        data = request.data
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.middle_name = data.get('middle_name', user.middle_name)
        user.birth_date = data.get('birth_date', user.birth_date)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request):
        user = User.objects.filter(phone_number=request.data.get('phone_number'))
        if not user:
            return Response(data={'message': 'We haven\'t user with such phone number.'},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(user)
        return Response(data={'message': 'User deleted successfully!'},
                        status=status.HTTP_200_OK)
