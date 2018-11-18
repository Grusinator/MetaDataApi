from django.db import models
from django.conf import settings
from enum import Enum
from inflection import camelize
from datetime import datetime


from django.core.exceptions import (
    ValidationError,
    ObjectDoesNotExist, MultipleObjectsReturned)

from MetaDataApi.metadata.custom_storages import MediaStorage


from MetaDataApi.metadata.models import (
    Attribute, Object, ObjectRelation, Schema
)

from MetaDataApi.metadata.utils import BuildSearchArgsFromJson, DictUtils


class CategoryTypes(Enum):
    test = "test"
    speech = "speech"
    diet = "diet"
    sleep = "sleep"
    phys_act = "phys_act"
    ment_act = "ment_act"
    body_meas = "body_meas"

    def force_value(self, input):
        for category in CategoryTypes:
            if input == category.name:
                return category.value
            elif input == category.value:
                return category.value


# Create your models here.
""" used for uploading data before processed into structured data"""


class RawData(models.Model):
    starttime = models.DateTimeField(auto_now=False)
    stoptime = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(
        upload_to='datapoints/images', null=True, blank=True)
    audio = models.FileField(
        upload_to='datapoints/audio', null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    std = models.FloatField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s " % (
            self.owner.username,
            self.starttime.strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        app_label = 'metadata'


class RDFDataDump(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    rdf_file = models.FileField(
        upload_to='datapoints/audio', storage=MediaStorage())
    schema = models.ForeignKey(
        Schema, related_name='data_dumps', on_delete=models.CASCADE)


# instance classes

class BaseInstance(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ObjectInstance(BaseInstance):
    base = models.ForeignKey(Object, on_delete=models.CASCADE)

    def __str__(self):
        return "Oi:%s.%s" % (self.base.schema.label, self.base.label)

    @classmethod
    def exists(cls, label, children={}):
        arg_builder = BuildSearchArgsFromJson()
        args = arg_builder.build(children)
        args["label"] = label
        args = BuildSearchArgsFromJson.modify_keys_in_dict(
            args, lambda x: "base__" + x)

        try:
            return cls.objects.get(**args)
        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            return None

    # def object_childrens_to_json(self):
    #     raise NotImplementedError

    class Meta:
        app_label = 'metadata'
        default_related_name = '%(model_name)s'


class ObjectRelationInstance(BaseInstance):
    base = models.ForeignKey(ObjectRelation, on_delete=models.CASCADE)

    from_object = models.ForeignKey(
        ObjectInstance,
        related_name='to_relations', on_delete=models.CASCADE)
    to_object = models.ForeignKey(
        ObjectInstance,
        related_name='from_relations', on_delete=models.CASCADE)

    def __str__(self):
        return "Ri:%s - %s - %s" % (
            self.base.from_object.label,
            self.base.label,
            self.base.to_object.label)

    class Meta:
        app_label = 'metadata'
        default_related_name = '%(model_name)s'

    # custom restrictions on foreign keys to make sure the instances are of
    # the right meta object type
    def save(self, *args, **kwargs):
        if self.from_object.base != self.base.from_object:
            raise ValidationError(
                "from_object instance must match the base from_object")
        if self.to_object.base != self.base.to_object:
            raise ValidationError(
                "to_object instance must match the base to_object")

        return super(ObjectRelationInstance, self).save(*args, **kwargs)


# Attribute Instances

# this is the class that we are going to inherit from
class BaseAttributeInstance(BaseInstance):
    base = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    object = models.ForeignKey(ObjectInstance, on_delete=models.CASCADE)

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
    def exists(cls, label, parrent_object_pk, value):
        # AttributeInstance = DictUtils.inverse_dict(
        #     cls.att_inst_to_type_map, data_type)
        args = {
            "base__label": label,
            "value": value,
            "object__pk": parrent_object_pk
        }
        try:
            return cls.objects.get(**args)
        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            return None

    class Meta(BaseInstance.Meta):
        abstract = True


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
    value = models.ImageField()

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
