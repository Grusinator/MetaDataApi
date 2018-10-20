from django.db import models
from django.conf import settings
from enum import Enum

from MetaDataApi.metadata.models import (
    Attribute, Object, ObjectRelation, Schema
)

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
    metadata = models.ForeignKey(MetaData, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s - %s " % (
            self.metadata.category,
            self.metadata.label,
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


class TemporalFloatAttributeInstance(models.Model):
    # must have timestamp and value
    starttime = models.DateTimeField(auto_now=False)
    # stoptime defines the interval if any
    stoptime = models.DateTimeField(null=True, blank=True)
    value = models.FloatField()
    std = models.FloatField(null=True, blank=True)
    base = models.ForeignKey(
        Attribute, related_name="temporal_float_attributes_insts",
        on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)
    object = models.ForeignKey(
        ObjectInstance, related_name='temp_float_attributes',
        on_delete=models.CASCADE)

    class Meta:
        app_label = 'datapoints'


class TemporalStringAttributeInstance(models.Model):
    # must have timestamp and value
    starttime = models.DateTimeField(auto_now=False)
    # stoptime defines the interval if any
    stoptime = models.DateTimeField(null=True, blank=True)
    value = models.FloatField()
    std = models.FloatField(null=True, blank=True)
    base = models.ForeignKey(
        Attribute, related_name="temporal_string_attribute_insts",
        on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)
    object = models.ForeignKey(
        ObjectInstance, related_name='temp_string_attributes',
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
