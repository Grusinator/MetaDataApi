from datetime import datetime
from enum import Enum

from PIL import Image
from django.core.files import File
from django.db import models

from MetaDataApi.utils import DictUtils
from metadata.models.meta.BaseMeta import BaseMeta
from metadata.models.meta.SchemaNode import SchemaNode


class SchemaAttribute(BaseMeta):
    class DataType(Enum):
        DateTime = "DateTime"
        Number = "Number"
        Integer = "Integer"
        Boolean = "Boolean"
        String = "String"
        File = "File"
        Image = "Image"
        Undefined = "Undefined"

        def __str__(self):
            return self.value

    data_type_map = {
        datetime: DataType.DateTime.value,
        float: DataType.Number.value,
        int: DataType.Integer.value,
        bool: DataType.Boolean.value,
        str: DataType.String.value,
        File: DataType.File.value,
        Image: DataType.Image.value,
        type(None): DataType.Undefined.value
    }
    data_type_choises = [(x, x) for x in data_type_map.values()]
    # data_type_choises = [(tag, tag.value) for tag in DataType]

    # db Fields
    data_type = models.TextField(choices=data_type_choises)
    object = models.ForeignKey(
        SchemaNode, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return "A:%s.%s" % (self.object.label, self.label)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    class Meta:
        unique_together = ('label', 'object')
        app_label = 'metadata'

    @classmethod
    def datatype_to_data_object(cls, data_type: DataType):
        return DictUtils.inverse_dict(cls.data_type_map, data_type.value)

    @classmethod
    def exists_by_label(cls, label: str, object__label: str):
        search_args = dict(locals())
        search_args.pop("cls")
        return cls.get_schema_item(cls, **search_args)

    @classmethod
    def exists(cls, att):
        return cls.exists_by_label(att.label, att.object.label)

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def assert_data_type(cls, attribute, data_type):
        data_type_name = cls.data_type_map[data_type]
        msg = f"the found attr: {attribute.label} has type {attribute.data_type}," \
              f" but it must be a {str(data_type_name)}"
        assert attribute.data_type == data_type_name, msg
