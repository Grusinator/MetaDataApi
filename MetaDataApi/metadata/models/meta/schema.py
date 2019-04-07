from django.db import models

from MetaDataApi.metadata.custom_storages import MediaStorage
from MetaDataApi.metadata.models.meta import BaseMeta


class Schema(models.Model):
    label = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    rdfs_file = models.FileField(
        upload_to="schemas",
        null=True, blank=True, storage=MediaStorage())

    def __str__(self):
        return "S:" + self.label

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.url == other.url and \
                   self.label == other.label
        else:
            return False

    @classmethod
    def exists(cls, label):
        BaseMeta.get_schema_item(cls, label=label)

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        app_label = 'metadata'
