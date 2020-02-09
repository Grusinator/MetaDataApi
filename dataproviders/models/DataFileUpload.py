from django.db import models

from dataproviders.models.DataFileSourceBase import DataFileSourceBase
from dataproviders.models.DataProvider import DataProvider

data_file_upload_on_save_methods = []


class DataFileUpload(DataFileSourceBase):
    data_provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)

    class Meta(DataFileSourceBase.Meta):
        default_related_name = '%(model_name)s'

    def execute_on_save_methods(self):
        for method in data_file_upload_on_save_methods:
            method(self)
