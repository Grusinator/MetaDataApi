from django.db import models

from dataproviders.models import DataProvider
from dataproviders.models.DataFileSourceBase import DataFileSourceBase

data_file_upload_on_save_methods = []


class DataFileUpload(DataFileSourceBase):
    data_provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)

    class Meta(DataFileSourceBase.Meta):
        default_related_name = '%(model_name)s'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.execute_on_save_methods()

    def execute_on_save_methods(self):
        for method in data_file_upload_on_save_methods:
            method(self)
