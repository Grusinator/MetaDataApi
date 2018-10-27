from django.db import models
from django.conf import settings
from enum import Enum

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

# instance classes


class ObjectInstance(models.Model):
    base = models.ForeignKey(
        Object,
        related_name='object_instances', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "O:%s.%s" % (self.base.schema.label, self.base.label)

    class Meta:
        app_label = 'datapoints'


class GenericAttributeInstance(models.Model):
    base = models.ForeignKey(
        Attribute,
        related_name='attribute_instances', on_delete=models.CASCADE)
    value = models.TextField()
    object = models.ForeignKey(
        ObjectInstance, related_name='attributes', on_delete=models.CASCADE)

    def __str__(self):
        return "A:%s.%s:%s" % (self.base.object.label, self.base.label, self.value)

    class Meta:
        app_label = 'datapoints'


class DateTimeAttributeInstance(models.Model):
    # must have timestamp and value
    value = models.DateTimeField()
    base = models.ForeignKey(
        Attribute, related_name="datetime_attributes_insts",
        on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)
    object = models.ForeignKey(
        ObjectInstance, related_name='datetime_attributes',
        on_delete=models.CASCADE)

    class Meta:
        app_label = 'datapoints'


class BoolAttributeInstance(models.Model):
    # must have timestamp and value
    value = models.BooleanField()
    base = models.ForeignKey(
        Attribute, related_name="bool_attributes_insts",
        on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)
    object = models.ForeignKey(
        ObjectInstance, related_name='bool_attributes',
        on_delete=models.CASCADE)

    class Meta:
        app_label = 'datapoints'


class IntAttributeInstance(models.Model):
    # must have timestamp and value
    value = models.IntegerField()
    base = models.ForeignKey(
        Attribute, related_name="int_attributes_insts",
        on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)
    object = models.ForeignKey(
        ObjectInstance, related_name='int_attributes',
        on_delete=models.CASCADE)

    class Meta:
        app_label = 'datapoints'


class FloatAttributeInstance(models.Model):
    value = models.FloatField()
    std = models.FloatField(null=True, blank=True)
    base = models.ForeignKey(
        Attribute, related_name="float_attributes_insts",
        on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)
    object = models.ForeignKey(
        ObjectInstance, related_name='float_attributes',
        on_delete=models.CASCADE)

    class Meta:
        app_label = 'datapoints'


class StringAttributeInstance(models.Model):
    value = models.TextField()
    base = models.ForeignKey(
        Attribute, related_name="string_attribute_insts",
        on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)
    object = models.ForeignKey(
        ObjectInstance, related_name='string_attributes',
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s - %s " % (
            self.metadata.category,
            self.metadata.label,
            self.owner.username,
            self.starttime.strftime("%Y-%m-%d %H:%M:%S"))

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
        return "R:%s - %s - %s" % (
            self.base.from_object.label,
            self.base.label,
            self.base.to_object.label)

    class Meta:
        app_label = 'datapoints'
