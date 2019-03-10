from django.db import models

from metadata.custom_storages import MediaStorage


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

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        app_label = 'metadata'
