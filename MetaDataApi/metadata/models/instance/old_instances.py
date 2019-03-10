from enum import Enum

from django.conf import settings
from django.db import models


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
