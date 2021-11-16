from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import ugettext as _


class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(
            years=range(datetime.now().year, datetime.now().year - 120, -1)
        ),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Email / Phone Number"))
    remember_me = forms.BooleanField(required=False)
    error_messages = {
        "invalid_login": _(
            "Please enter a correct email / phone number and password. "
            "Note that both fields may be case-sensitive."
        ),
        "inactive": _("Sorry, your has been locked by an administrator."),
    }


class EditForm(forms.ModelForm):
    birth_date = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(
            years=range(datetime.now().year, datetime.now().year - 120, -1)
        ),
    )

    class Meta:
        model = get_user_model()
        fields = (
            # "profile_pic",
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "phone_number",
        )
