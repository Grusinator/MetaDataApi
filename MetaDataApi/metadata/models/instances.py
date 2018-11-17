from django.db import models
from django.conf import settings
from enum import Enum
from inflection import camelize

from django.core.exceptions import ValidationError

from MetaDataApi.metadata.custom_storages import MediaStorage


from MetaDataApi.metadata.models import (
    Attribute, Object, ObjectRelation, Schema
)


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
        app_label = 'datapoints'


class RDFDataDump(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    rdf_file = models.FileField(
        upload_to='datapoints/audio', storage=MediaStorage())
    schema = models.ForeignKey(
        Schema, related_name='data_dumps', on_delete=models.CASCADE)


# instance classes


class ObjectInstance(models.Model):
    base = models.ForeignKey(
        Object,
        related_name='object_instances', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Oi:%s.%s" % (self.base.schema.label, self.base.label)

    class Meta:
        app_label = 'datapoints'


class ObjectRelationInstance(models.Model):
    base = models.ForeignKey(
        ObjectRelation,
        related_name='object_relation_instances', on_delete=models.CASCADE)
    from_object = models.ForeignKey(
        ObjectInstance,
        related_name='to_relations', on_delete=models.CASCADE)
    to_object = models.ForeignKey(
        ObjectInstance,
        related_name='from_relations', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Ri:%s - %s - %s" % (
            self.base.from_object.label,
            self.base.label,
            self.base.to_object.label)

    class Meta:
        app_label = 'datapoints'

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


# this is the class that we are going to inherit from
class BaseAttributeInstance(models.Model):
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


# we call the base attribute instance string because it is
# the most generic one, just overwrite value, when inheriting
class StringAttributeInstance(BaseAttributeInstance):
    value = models.TextField()
    object = models.ForeignKey(
        ObjectInstance, related_name="string_attributes",
        on_delete=models.CASCADE)
    base = models.ForeignKey(
        Attribute,
        related_name='string_instances', on_delete=models.CASCADE)


class DateTimeAttributeInstance(BaseAttributeInstance):
    # must have timestamp and value
    value = models.DateTimeField()
    object = models.ForeignKey(
        ObjectInstance, related_name="datetime_attributes",
        on_delete=models.CASCADE)
    base = models.ForeignKey(
        Attribute,
        related_name='date_time_instances', on_delete=models.CASCADE)


class BoolAttributeInstance(BaseAttributeInstance):
    # must have timestamp and value
    value = models.BooleanField()
    base = models.ForeignKey(
        Attribute, related_name="bool_attributes_insts",
        on_delete=models.CASCADE)
    object = models.ForeignKey(
        ObjectInstance, related_name='bool_attributes',
        on_delete=models.CASCADE)
    base = models.ForeignKey(
        Attribute,
        related_name='bool_instances', on_delete=models.CASCADE)


class IntAttributeInstance(models.Model):
    # must have timestamp and value
    value = models.IntegerField()
    base = models.ForeignKey(
        Attribute, related_name="int_attributes_insts",
        on_delete=models.CASCADE)

    object = models.ForeignKey(
        ObjectInstance, related_name='int_attributes',
        on_delete=models.CASCADE)


class FloatAttributeInstance(BaseAttributeInstance):
    value = models.FloatField()
    base = models.ForeignKey(
        Attribute, related_name="float_attributes_insts",
        on_delete=models.CASCADE)
    object = models.ForeignKey(
        ObjectInstance, related_name='float_attributes',
        on_delete=models.CASCADE)


class ImageAttributeInstance(BaseAttributeInstance):
    value = models.ImageField()
    base = models.ForeignKey(
        Attribute, related_name="image_attribute_insts",
        on_delete=models.CASCADE)
    object = models.ForeignKey(
        ObjectInstance, related_name='image_attributes',
        on_delete=models.CASCADE)
