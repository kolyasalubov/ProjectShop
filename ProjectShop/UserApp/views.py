from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views, get_user_model
from django.views import generic
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from braces.views import AnonymousRequiredMixin

from UserApp.forms import LoginForm, RegisterForm, EditForm


class LoginView(AnonymousRequiredMixin, auth_views.LoginView):
    form_class = LoginForm
    template_name = 'UserApp/login.html'


class RegisterView(AnonymousRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = RegisterForm
    template_name = 'UserApp/register.html'
    success_url = reverse_lazy('login')
    success_message = _("Congratulations! Your account has been created. You may sign in!")


class TemporalHomePageView(TemplateView):
    template_name = 'UserApp/home.html'


class CustomUpdateView(generic.edit.SingleObjectTemplateResponseMixin,
                       generic.edit.ModelFormMixin,
                       generic.edit.ProcessFormView):

    def get(self, request, *args, **kwargs):
        self.object = request.user
        return super().get(request, *args, kwargs)

    def post(self, request, *args, **kwargs):
        self.object = request.user
        return super().post(request, *args, kwargs)


class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, CustomUpdateView):
    form_class = EditForm
    model = get_user_model
    template_name = 'UserApp/profile.html'
    success_url = reverse_lazy('profile')
    success_message = _("Your account has been updated!")
