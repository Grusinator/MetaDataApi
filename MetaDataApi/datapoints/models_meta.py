from django.db import models
from django.conf import settings
from enum import Enum
from inflection import camelize

from django.core.exceptions import ValidationError

from MetaDataApi.metadata.custom_storages import MediaStorage


from MetaDataApi.metadata.models import (
    Attribute, Object, ObjectRelation, Schema
)


DateTimeAttributeInstance = AttributeInstanceFactory(
    "date_time", models.DateTimeField())


class MetaAttribute(type):

    @classmethod
    def __prepare__(metacls, name, bases, **kargs):
        # kargs = {"myArg1": 1, "myArg2": 2}
        return super().__prepare__(name, bases, **kargs)

    def __new__(metacls, name, bases, namespace, **kargs):
        # kargs = {"myArg1": 1, "myArg2": 2}
        namespace["value"] = kargs["value_type"]

        base = kargs["base"]
        bases = (base,)

        # here starts the creation of the Attribute instance
        name_prefix = kargs["name_prefix"].lower()
        name = camelize(name_prefix + "_attribute_instance")

        return super().__new__(metacls, name, bases, namespace)
        # DO NOT send "**kargs" to "type.__new__".  It won't catch them and
        # you'll get a "TypeError: type() takes 1 or 3 arguments" exception.

    def __init__(cls, name, bases, namespace, myArg1=7, **kargs):
        # myArg1 = 1  #Included as an example of capturing metaclass args as positional args.
        # kargs = {"myArg2": 2}
        super().__init__(name, bases, namespace)


class FloatAttributeInstance(
        metaclass=MetaAttribute,
        name_prefix="float",
        value_type=models.FloatField,
        base=BaseAttributeInstance):
    pass


def AttributeInstanceFactory(name_prefix: str, django_value_field):
    class BaseAttributeInstance(models.Model):
        # TODO base all other classes on this one
        base = models.ForeignKey(Attribute, on_delete=models.CASCADE)
        object = models.ForeignKey(ObjectInstance, on_delete=models.CASCADE)
        owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  null=True, on_delete=models.CASCADE)

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

        class Meta:
            app_label = 'datapoints'

    # here starts the creation of the Attribute instance
    name_prefix = name_prefix.lower()
    name = camelize(name_prefix + "_attribute_instance")

    AttributeInstance = type(
        name,
        (BaseAttributeInstance,),
        {"value": django_value_field()}
    )
    # update the related names
    AttributeInstance.object.related_name = name_prefix + "_attr_insts"
    AttributeInstance.base.related_name = name_prefix + "_attr_insts"

    return AttributeInstance
