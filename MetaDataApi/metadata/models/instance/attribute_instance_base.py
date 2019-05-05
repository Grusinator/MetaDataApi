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
        if isinstance(data_type, Attribute.DataType):
            data_type = data_type.value
        # TODO fix odd
        if data_type == "string":
            data_type = "String"
        datatype = DictUtils.inverse_dict(Attribute.data_type_map, data_type)
        return DictUtils.inverse_dict(BaseAttributeInstance.att_inst_to_type_map, datatype)

    @classmethod
    def get_data_type(cls):
        return cls.att_inst_to_type_map[cls]

    @classmethod
    def get_all_instance_types(cls):
        return list(cls.att_inst_to_type_map.keys())

    @classmethod
    def get_all_instances_from_base(cls, att_base: Attribute):
        instance_types = cls.get_all_instance_types()
        related_names = [instance_type.__name__.lower() for instance_type in instance_types]
        instances = []
        for related_name in related_names:
            related_manager = getattr(att_base, related_name)
            instances.extend(related_manager.all())
        return instances
