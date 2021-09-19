from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
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


@login_required
def profile(request):
    """
    User must be logged in to view the profile page. Otherwise, the user is redirected to the log in page.
    If POST request is received then validate and update the form data.
    """
    if request.method == 'POST':
        form = EditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been successfully updated!')
            return redirect('profile')
    else:
        form = EditForm(instance=request.user)

    return render(request, 'UserApp/profile.html', {'form': form})
