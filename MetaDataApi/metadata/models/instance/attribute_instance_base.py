from django.core.exceptions import ValidationError
from django.db import models

from MetaDataApi.metadata.models.meta import Attribute
from MetaDataApi.metadata.utils import DictUtils
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils
from .instance_base import BaseInstance


class BaseAttributeInstance(BaseInstance):
    base = models.ForeignKey('Attribute', on_delete=models.CASCADE)
    object = models.ForeignKey('ObjectInstance', on_delete=models.CASCADE)

    # the dictionary is populated after init of specific attribute instances
    att_inst_to_type_map = {}

    def __str__(self):
        return "Ai:%s.%s:%s" % (self.base.object.label, self.base.label,
                                str(self.value))

    class Meta(BaseInstance.Meta):
        abstract = True

    # custom restrictions on foreign keys to make sure the instances are of
    # the right meta object type
    def save(self, *args, **kwargs):
        if self.object.base != self.base.object:
            raise ValidationError(
                "object instance must match the base object")

        return super(BaseAttributeInstance, self).save(*args, **kwargs)

    @classmethod
    def exists_by_label(cls, base__label, object__pk, value):
        search_args = dict(locals())
        search_args.pop("cls")

        return DjangoModelUtils.get_object_or_none(cls, **search_args)

    @classmethod
    def get_attribute_instance_from_data_type(cls, data_type: Attribute.DataType):
        datatype = DictUtils.inverse_dict(Attribute.data_type_map, data_type.value)
        return DictUtils.inverse_dict(BaseAttributeInstance.att_inst_to_type_map, datatype)

    @classmethod
    def get_attribute_instance_from_type(cls, type_as_string: str):
        datatype = DictUtils.inverse_dict(Attribute.data_type_map, str(type_as_string))
        return DictUtils.inverse_dict(BaseAttributeInstance.att_inst_to_type_map, datatype)
