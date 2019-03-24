from django.db import models

from MetaDataApi.metadata.models.meta import BaseMeta


class UnmappedObject(BaseMeta):
    parrent_label = models.TextField()
    childrens = models.TextField()

    class Meta:
        app_label = 'metadata'
