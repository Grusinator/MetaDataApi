from django import forms

from dataproviders.models.FileUpload import FileUpload


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('file',)
