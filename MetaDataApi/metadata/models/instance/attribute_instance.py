from datetime import datetime

from django.db import models

from metadata.custom_storages import MediaStorage
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
    value = models.ImageField(upload_to="images", storage=MediaStorage())

    class Meta(BaseAttributeInstance.Meta):
        default_related_name = '%(model_name)s'


class FileAttributeInstance(BaseAttributeInstance):
    value = models.FileField(upload_to="datafiles", storage=MediaStorage())

    class Meta(BaseAttributeInstance.Meta):
        default_related_name = '%(model_name)s'


# define the mapping between type and InstanceClass
BaseAttributeInstance.att_inst_to_type_map = {
    StringAttributeInstance: str,
    DateTimeAttributeInstance: datetime,
    FloatAttributeInstance: float,
    IntAttributeInstance: int,
    BoolAttributeInstance: bool,
}
