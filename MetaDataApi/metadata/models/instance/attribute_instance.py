from datetime import datetime

from PIL import Image
from django.core.files import File
from django.db import models
from django.urls import reverse

from MetaDataApi.metadata.custom_storages import PrivateMediaStorage
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils
from .attribute_instance_base import BaseAttributeInstance


class StringAttributeInstance(BaseAttributeInstance):
    value = models.TextField()

    class Meta(BaseAttributeInstance.Meta):
        default_related_name = '%(model_name)s'


class DateTimeAttributeInstance(BaseAttributeInstance):
    # must have timestamp and value
    value = models.DateTimeField()

    class Meta(BaseAttributeInstance.Meta):
        default_related_name = '%(model_name)s'


class BoolAttributeInstance(BaseAttributeInstance):
    # must have timestamp and value
    value = models.BooleanField()

    class Meta(BaseAttributeInstance.Meta):
        default_related_name = '%(model_name)s'


class IntAttributeInstance(BaseAttributeInstance):
    # must have timestamp and value
    value = models.IntegerField()

    class Meta(BaseAttributeInstance.Meta):
        default_related_name = '%(model_name)s'


class FloatAttributeInstance(BaseAttributeInstance):
    value = models.FloatField()

    class Meta(BaseAttributeInstance.Meta):
        default_related_name = '%(model_name)s'


class ImageAttributeInstance(BaseAttributeInstance):
    value = models.ImageField(upload_to="images", storage=PrivateMediaStorage())

    class Meta(BaseAttributeInstance.Meta):
        default_related_name = '%(model_name)s'


class FileAttributeInstance(BaseAttributeInstance):
    storage_path = "datafiles/"
    value = models.FileField(upload_to=storage_path, storage=PrivateMediaStorage())

    def __str__(self):
        return "Ai:%s.%s:%s" % (self.base.object.label, self.base.label,
                                str(self.value.file.name))

    def get_internal_view_url(self):
        return reverse('datafile', args=[str(self.value).split("/")[1]])


    class Meta(BaseAttributeInstance.Meta):
        default_related_name = '%(model_name)s'

    def read_as_str(self):
        return DjangoModelUtils.convert_file_to_str(self.value.file)


# define the mapping between type and InstanceClass
BaseAttributeInstance.att_inst_to_type_map = {
    StringAttributeInstance: str,
    DateTimeAttributeInstance: datetime,
    FloatAttributeInstance: float,
    IntAttributeInstance: int,
    BoolAttributeInstance: bool,
    FileAttributeInstance: File,
    ImageAttributeInstance: Image
}
