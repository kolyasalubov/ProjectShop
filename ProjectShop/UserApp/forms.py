from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import ugettext as _

from datetime import datetime


class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(required=False,
                                 widget=forms.SelectDateWidget(years=range(datetime.now().year,
                                                                           datetime.now().year - 120,
                                                                           -1)
                                                               )
                                 )

    class Meta:
        model = get_user_model()
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'birth_date', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Email / Phone Number'))
    error_messages = {
        'invalid_login': _("Please enter a correct email / phone number and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("Sorry, your has been locked by an administrator."),
    }


class EditForm(forms.ModelForm):
    birth_date = forms.DateField(required=False,
                                 widget=forms.SelectDateWidget(years=range(datetime.now().year,
                                                                           datetime.now().year - 120,
                                                                           -1)
                                                               )
                                 )

    class Meta:
        model = get_user_model()
        fields = ('profile_pic', 'phone_number', 'first_name', 'last_name', 'birth_date')
