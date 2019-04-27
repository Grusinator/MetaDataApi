from django.core.files.base import ContentFile
from django.db import models

from MetaDataApi.metadata.custom_storages import PublicMediaStorage
from MetaDataApi.metadata.models.meta import BaseMeta
from MetaDataApi.metadata.utils.common_utils import StringUtils


class Schema(models.Model):
    label = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    rdfs_file = models.FileField(
        upload_to="schemas",
        null=True, blank=True, storage=PublicMediaStorage())

    def __str__(self):
        return "S:" + str(self.label)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.url == other.url and \
                   self.label == other.label
        else:
            return False

    @staticmethod
    def create_new_empty_schema(schema_label):
        schema = Schema()
        schema.label = StringUtils.standardize_string(schema_label)
        schema.description = ""
        schema.url = "temp"
        # quick fix for saving without conflicting with unique url

        # create a dummy file
        content = ContentFile("")
        schema.rdfs_file.save(schema_label + ".ttl", content)
        schema.url = schema.rdfs_file.url
        schema.save()

        return schema

    @classmethod
    def exists_by_label(cls, label: str):
        return BaseMeta.get_schema_item(cls, label=label)

    @classmethod
    def exists(cls, schema):
        return cls.exists_by_label(schema.label)

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        app_label = 'metadata'

    def create_if_not_exists(self):
        item_found = self.exists(self)
        if not item_found:
            self.save()
            return self
        else:
            return item_found
