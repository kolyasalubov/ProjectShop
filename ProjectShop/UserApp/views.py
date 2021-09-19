from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.views import generic
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from UserApp.forms import LoginForm, RegisterForm


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'UserApp/login.html'


class RegisterView(SuccessMessageMixin, generic.CreateView):
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
