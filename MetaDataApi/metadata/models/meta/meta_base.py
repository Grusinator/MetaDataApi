from django.db import models


class BaseMeta(models.Model):
    label = models.TextField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'metadata'
