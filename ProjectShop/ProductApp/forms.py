from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from ProductApp.models import AdvancedProductDescription


class AdvancedDescriptionForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = AdvancedProductDescription
        fields = "__all__"
