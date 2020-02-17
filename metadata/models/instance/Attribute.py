from datetime import datetime

# from PIL import Image
from django.core.files import File
from django.db import models
from django.urls import reverse

from MetaDataApi.custom_storages import PrivateMediaStorage
from MetaDataApi.utils.django_utils import django_file_utils
from metadata.models.meta import SchemaAttribute
from .BaseAttribute import BaseAttribute


class StringAttribute(BaseAttribute):
    data_type = SchemaAttribute.DataType.String
    value = models.TextField()

    class Meta(BaseAttribute.Meta):
        default_related_name = '%(model_name)s'


class DateTimeAttribute(BaseAttribute):
    data_type = SchemaAttribute.DataType.DateTime
    value = models.DateTimeField()

    class Meta(BaseAttribute.Meta):
        default_related_name = '%(model_name)s'


class BoolAttribute(BaseAttribute):
    data_type = SchemaAttribute.DataType.Boolean
    value = models.BooleanField()

    class Meta(BaseAttribute.Meta):
        default_related_name = '%(model_name)s'


class IntAttribute(BaseAttribute):
    data_type = SchemaAttribute.DataType.Integer
    value = models.IntegerField()

    class Meta(BaseAttribute.Meta):
        default_related_name = '%(model_name)s'


class FloatAttribute(BaseAttribute):
    data_type = SchemaAttribute.DataType.Number
    value = models.FloatField()

    class Meta(BaseAttribute.Meta):
        default_related_name = '%(model_name)s'


class ImageAttribute(BaseAttribute):
    data_type = SchemaAttribute.DataType.Image
    value = models.ImageField(
        upload_to="images", storage=PrivateMediaStorage())

    class Meta(BaseAttribute.Meta):
        default_related_name = '%(model_name)s'


class FileAttribute(BaseAttribute):
    data_type = SchemaAttribute.DataType.File
    storage_path = "datafiles/"
    value = models.FileField(upload_to=storage_path,
                             storage=PrivateMediaStorage())

    def __str__(self):
        return "Ai:%s.%s:%s" % (self.base.object.label, self.base.label,
                                str(self.value.file.name))

    def get_internal_view_url(self):
        return reverse('datafile', args=[str(self.value).split("/")[1]])

    class Meta(BaseAttribute.Meta):
        default_related_name = '%(model_name)s'

    def read_as_str(self):
        return django_file_utils.convert_file_to_str(self.value.file)


# define the mapping between type and InstanceClass
BaseAttribute.att_inst_to_type_map = {
    StringAttribute: str,
    DateTimeAttribute: datetime,
    FloatAttribute: float,
    IntAttribute: int,
    BoolAttribute: bool,
    FileAttribute: File,
    # ImageAttribute: Image
}
