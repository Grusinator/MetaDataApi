from django.db import models

from MetaDataApi.dataproviders.models.Endpoint import Endpoint
from MetaDataApi.metadata.custom_storages import PrivateMediaStorage


class DataDump(models.Model):
    date_downloaded = models.DateField(auto_now=True)
    endpoint = models.ForeignKey(Endpoint, related_name="data_dumps", on_delete=models.CASCADE)
    file = models.FileField(upload_to="datafiles/", storage=PrivateMediaStorage())

    def __str__(self):
        return f"{self.date_downloaded} - {self.endpoint} - {self.file}"
