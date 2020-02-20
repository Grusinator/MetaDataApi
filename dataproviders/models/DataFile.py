from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from djcelery_model.models import TaskMixin
from jsonfield import JSONField

from MetaDataApi.custom_storages import PrivateMediaStorage
from MetaDataApi.utils import JsonUtils
from dataproviders.models.DataProvider import DataProvider

data_file_on_save_methods = []


class DataFile(TaskMixin, models.Model):
    date_created = models.DateField(auto_now=True)
    data_file = models.FileField(upload_to=settings.DATAFILE_STORAGE_PATH, storage=PrivateMediaStorage())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)
    label_info = JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.date_created} - {self.data_file}"

    def get_internal_view_url(self):
        return reverse('data_fetch_detail', args=[str(self.data_file).split("/")[1]])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.execute_on_save_methods()

    def read_data(self):
        return JsonUtils.loads(self.data_file.read())

    def execute_on_save_methods(self):
        for method in data_file_on_save_methods:
            method(self)
