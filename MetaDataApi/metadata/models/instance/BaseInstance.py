from django.conf import settings
from django.db import models


class BaseInstance(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        app_label = 'metadata'
