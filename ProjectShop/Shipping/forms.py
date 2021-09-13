from django import forms
from .models import ShippingModel

# creating a form
class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingModel
        # fields of ShippingModel
        fields = [
            "postal_code",
            "country",
            "region",
            "city",
            "post_office",
            # "user"
        ]
