from django.db import models
from django.conf import settings
from enum import Enum

# Create your models here.


# class CategoryTypes(Enum):
#    TST = "test"
#    WGT = "weight"
#    SPC = "speech_audio"
#    SHT = "shit_cam"
#    FOD = "food_picture"
#    HRT = "heart_rate"

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

# class Datapoint(models.Model):
#     datetime = models.DateTimeField(auto_now=True)
#     category = models.TextField(null=False, blank=False, max_length=3,
#         choices=[(tag.value, tag.name) for tag in CategoryTypes])
#     image = models.ImageField(upload_to='datapoints/images', null=True,
#       blank=True)
#     audio = models.FileField(upload_to='datapoints/audio', null=True,
# blank=True)
#     source_device = models.TextField(null=False, blank=False)
#     value = models.FloatField(null=True, blank=True)
#     text_from_audio = models.TextField(null=True, blank=True)
#     #dynamic_attributes = models.TextField(null=True, blank=True)
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
# on_delete=models.CASCADE)

#     def __str__(self):
#         return "%i - %s - %s - %s "%(self.id, self.category,
# self.owner.username, self.datetime.strftime("%Y-%m-%d %H:%M:%S"))

#     def __eq__(self, other):
#         selfdict = self.__dict__.copy()
#         otherdict = other.__dict__.copy()

#         selfdict.pop("_state")
#         otherdict.pop("_state")
#         selfdict.pop("datetime")
#         otherdict.pop("datetime")

#         return selfdict == otherdict
#         #return self.__dict__ == other.__dict__

#     class Meta:
#         app_label = 'datapoints'


class MetaData(models.Model):
    # source category and label should be unique
    source = models.TextField()
    category = models.TextField(
        null=False, blank=False, max_length=10,
        choices=[(tag.value, tag.name) for tag in CategoryTypes])
    label = models.TextField(max_length=20)

    raw = models.BooleanField()
    value_unit = models.TextField(max_length=10)

    def __str__(self):
        return "%s: %s.%s " % (self.source, self.category, self.label)

    class Meta:
        app_label = 'datapoints'


class DatapointV2(models.Model):
    starttime = models.DateTimeField(auto_now=False)
    stoptime = models.DateTimeField(null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    std = models.FloatField(null=True, blank=True)
    metadata = models.ForeignKey(MetaData, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s - %s " % (
            self.metadata.category,
            self.metadata.label,
            self.owner.username,
            self.starttime.strftime("%Y-%m-%d %H:%M:%S"))


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
