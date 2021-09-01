from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import ugettext as _


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'birth_date', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Email / Phone Number'))


class EditForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'phone_number', 'first_name', 'last_name', 'birth_date')
