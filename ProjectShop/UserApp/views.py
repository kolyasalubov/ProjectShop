from braces.views import AnonymousRequiredMixin
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.base import TemplateView
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from UserApp.forms import LoginForm, RegisterForm, EditForm
from UserApp.models import User
from UserApp.permissions import IsAdminBot
from UserApp.serializers import UserSerializer, UserSerializerForPatch


class LoginView(AnonymousRequiredMixin, auth_views.LoginView):
    form_class = LoginForm
    template_name = "UserApp/login.html"


class RegisterView(AnonymousRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = RegisterForm
    template_name = "UserApp/register.html"
    success_url = reverse_lazy("login")
    success_message = _(
        "Congratulations! Your account has been created. You may sign in!"
    )


class LogoutView(auth_views.LogoutView):
    template_name = "UserApp/logout.html"


class PasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = 'UserApp/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = _("Congratulation! Your password has been updated!")


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "UserApp/password_reset.html"


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "UserApp/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "UserApp/password_reset_confirm.html"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "UserApp/password_reset_complete.html"


class TemporalHomePageView(TemplateView):
    template_name = "UserApp/home.html"


class CustomUpdateView(
    generic.edit.SingleObjectTemplateResponseMixin,
    generic.edit.ModelFormMixin,
    generic.edit.ProcessFormView,
):
    def get(self, request, *args, **kwargs):
        self.object = request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = request.user
        return super().post(request, *args, **kwargs)


class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, CustomUpdateView):
    form_class = EditForm
    model = get_user_model
    template_name = "UserApp/profile.html"
    success_url = reverse_lazy("profile")
    success_message = _("Your account has been updated!")


class BlacklistRefreshViewSet(viewsets.GenericViewSet):
    """
    A simple ViewSet for creating blacklist token from refresh token.
    """

    permission_classes = (IsAdminBot, IsAuthenticated)

    def create(self, request):
        try:
            refresh_token = RefreshToken(request.data.get("refresh"))
            refresh_token.blacklist()
        except TokenError as error:
            return Response(str(error), status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset made for our user.
    lookup_field = 'phone_number'
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "phone_number"
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == "PATCH":
            serializer_class = UserSerializerForPatch

        return serializer_class
