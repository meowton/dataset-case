from django import forms

from DataMatcher.models import FileUpload


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('description', 'file',)
