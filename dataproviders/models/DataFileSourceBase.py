from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from djcelery_model.models import TaskMixin

from MetaDataApi.custom_storages import PrivateMediaStorage
from dataproviders.models.DataFile import DataFile


class DataFileSourceBase(TaskMixin, models.Model):
    data_file_from_source = models.FileField(upload_to=settings.DATAFILE_STORAGE_PATH, storage=PrivateMediaStorage())
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refined_data_file = models.OneToOneField(DataFile, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True
