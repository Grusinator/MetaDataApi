from django.core.exceptions import ValidationError
from django.db import models

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

    # custom restrictions on foreign keys to make sure the instances are of
    # the right meta object type
    def save(self, *args, **kwargs):
        if self.object.base != self.base.object:
            raise ValidationError(
                "object instance must match the base object")

        return super(BaseAttributeInstance, self).save(*args, **kwargs)

    @classmethod
    def exists(cls, base__label, object__pk, value):
        search_args = dict(locals())
        search_args.pop("cls")

        return DjangoModelUtils.get_object_or_none(cls, **search_args)

    class Meta(BaseInstance.Meta):
        abstract = True
