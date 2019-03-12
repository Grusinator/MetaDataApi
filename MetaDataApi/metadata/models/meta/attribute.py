from datetime import datetime

from django.db import models

from metadata.models.meta.meta_base import BaseMeta
from metadata.models.meta.object import Object
from metadata.utils.django_model_utils import DjangoModelUtils


class Attribute(BaseMeta):
    data_type_map = {
        datetime: "datetime",
        float: "float",
        int: "int",
        bool: "bool",
        str: "string",
        type(None): "unknown"
    }
    data_type_choises = [(x, x) for x in data_type_map.values()]

    # db Fields
    data_type = models.TextField(choices=data_type_choises)
    data_unit = models.TextField()
    object = models.ForeignKey(Object, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return "A:%s.%s" % (self.object.label, self.label)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    @classmethod
    def exists(cls, label: str, object__label: str):
        search_args = dict(locals())
        search_args.pop("cls")
        return DjangoModelUtils.get_object_or_none(cls, **search_args)

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def assert_data_type(cls, attribute, data_type):
        data_type_name = cls.data_type_map[data_type]
        assert attribute.data_type == data_type_name, \
            "the found attr: %s has type %s, but it must be a %s" % (
                attribute.label,
                attribute.data_type,
                str(data_type_name)
            )

    class Meta:
        unique_together = ('label', 'object')
        app_label = 'metadata'
