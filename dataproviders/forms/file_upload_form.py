from django import forms

from dataproviders.models.DataFileUpload import DataFileUpload


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = DataFileUpload
        fields = ('data_file_from_source',)
