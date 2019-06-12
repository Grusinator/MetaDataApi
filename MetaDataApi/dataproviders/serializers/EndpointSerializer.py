from django.db import models
from django.urls import reverse
from django_enumfield import enum

from MetaDataApi.dataproviders.models.DataProvider import DataProvider
from MetaDataApi.dataproviders.models.RequestType import RequestType


class Endpoint(models.Model):
    endpoint_name = models.TextField()
    endpoint_url = models.TextField()
    request_type = enum.EnumField(RequestType, default=RequestType.GET)
    data_provider = models.ForeignKey(DataProvider, related_name="endpoints", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data_provider} - {self.endpoint_name} - {self.endpoint_url}"

    def get_internal_view_url(self):
        schema = self.data_provider.get_schema_for_provider()
        return reverse('endpoint_detail', args=[str(schema.label), self.endpoint_name])
