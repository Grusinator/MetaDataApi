from django.contrib.auth.models import User
from django.db import models

from MetaDataApi.custom_storages import PrivateMediaStorage
from dataproviders.models import DataProvider
from dataproviders.models.data_dump import datafile_storage_path


class FileUpload(models.Model):
    data_provider = models.ForeignKey(DataProvider, related_name="file_uploads", on_delete=models.CASCADE)
    file = models.FileField(upload_to=datafile_storage_path, storage=PrivateMediaStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
