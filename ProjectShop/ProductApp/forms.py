from django import forms
from ProductApp.models import Review
from ProductApp.models import AdvancedProductDescription
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ReviewForm(forms.ModelForm):

    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReviewForm, self).__init__(**kwargs)

    def save(self, commit=True):
        obj = super(ReviewForm, self).save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Review
        fields = ('comment','rating',)


class AdvancedDescriptionForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = AdvancedProductDescription
        fields = "__all__"
