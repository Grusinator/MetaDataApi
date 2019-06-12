from django.db import models

from MetaDataApi.dataproviders.models.Endpoint import Endpoint
from MetaDataApi.metadata.custom_storages import PrivateMediaStorage


class DataDump(models.Model):
    storage_path = "datafiles/"
    date_downloaded = models.DateField(auto_now=True)
    endpoint = models.ForeignKey(Endpoint, related_name="data_dumps", on_delete=models.CASCADE)
    file = models.FileField(upload_to=storage_path, storage=PrivateMediaStorage())
