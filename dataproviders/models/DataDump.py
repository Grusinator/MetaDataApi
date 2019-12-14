from django.db import models
from django.urls import reverse
from generic_serializer import SerializableModel

from MetaDataApi.custom_storages import PrivateMediaStorage
from dataproviders.models.Endpoint import Endpoint


class DataDump(models.Model, SerializableModel):
    storage_path = "datafiles/"
    date_downloaded = models.DateField(auto_now=True)
    endpoint = models.ForeignKey(Endpoint, related_name="data_dumps", on_delete=models.CASCADE)
    file = models.FileField(upload_to=storage_path, storage=PrivateMediaStorage())

    def __str__(self):
        return f"{self.date_downloaded} - {self.endpoint} - {self.file}"

    def get_internal_view_url(self):
        return reverse('data_dump_detail', args=[str(self.file).split("/")[1]])
