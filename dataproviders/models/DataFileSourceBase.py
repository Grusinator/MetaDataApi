from abc import ABCMeta, abstractmethod

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from djcelery_model.models import TaskMixin

from MetaDataApi.custom_storages import PrivateMediaStorage
from dataproviders.models.DataFile import DataFile


class DataFileSourceBase(TaskMixin, models.Model):
    __metaclass__ = ABCMeta
    data_file_from_source = models.FileField(upload_to=settings.DATAFILE_STORAGE_PATH, storage=PrivateMediaStorage())
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refined_data_file = models.OneToOneField(DataFile, on_delete=models.SET_NULL, null=True, blank=True)
    has_been_refined = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        return_obj = super().save(*args, **kwargs)
        self.execute_on_save_methods()
        return return_obj

    @abstractmethod
    def execute_on_save_methods(self):
        raise NotImplementedError()
