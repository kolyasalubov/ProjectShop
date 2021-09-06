from django import forms
from .models import ShippingModel


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingModel

        fields = [
            "postal_code",
            "country",
            "region",
            "city",
            "post_office",
            # "user"
        ]