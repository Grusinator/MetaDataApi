from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from djcelery_model.models import TaskMixin
from generic_serializer import SerializableModel

from MetaDataApi.custom_storages import PrivateMediaStorage
from dataproviders.models.Endpoint import Endpoint

data_dump_save_methods = []

datafile_storage_path = "datafiles/"

class DataDump(TaskMixin, SerializableModel, models.Model):
    date_downloaded = models.DateField(auto_now=True)
    endpoint = models.ForeignKey(Endpoint, related_name="data_dumps", on_delete=models.CASCADE)
    file = models.FileField(upload_to=datafile_storage_path, storage=PrivateMediaStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date_downloaded} - {self.endpoint} - {self.file}"

    def get_internal_view_url(self):
        return reverse('data_dump_detail', args=[str(self.file).split("/")[1]])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.execute_on_save_methods()

    def execute_on_save_methods(self):
        for method in data_dump_save_methods:
            method(self)
