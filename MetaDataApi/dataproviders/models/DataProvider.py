from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from django_enumfield import enum

from MetaDataApi.dataproviders.models.ApiTypes import ApiTypes
from MetaDataApi.metadata.models import Schema


class DataProvider(models.Model):
    provider_name = models.TextField(unique=True)
    api_type = enum.EnumField(ApiTypes, ApiTypes.OAUTH_REST)
    api_endpoint = models.TextField()
    data_provider_node = models.ForeignKey(
        "metadata.Node",
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="db_data_provider"
    )

    def get_internal_view_url(self):
        return reverse('provider_detail', args=[str(self.provider_name)])

    def get_webvowl_url(self):
        schema = self.get_schema_for_provider()
        return "http://visualdataweb.de/webvowl/#iri=" + schema.rdfs_file.url

    def __str__(self):
        return "%s - %s" % (self.provider_name, self.api_endpoint)

    def save(self, *args, **kwargs):
        if not Schema.exists_by_label(str(self.provider_name)):
            Schema.create_new_empty_schema(self.provider_name)

        super(DataProvider, self).save(*args, **kwargs)

    @classmethod
    def exists(cls, provider_name):
        try:
            return cls.objects.get(provider_name=provider_name)
        except ObjectDoesNotExist:
            return None

    def get_schema_for_provider(self):
        return Schema.objects.get(label=self.provider_name)

    class Meta:
        app_label = 'dataproviders'
