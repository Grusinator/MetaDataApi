
from django.db import models
from django.urls import reverse

from MetaDataApi.dataproviders.models.DataProvider import DataProvider
from MetaDataApi.dataproviders.models.RequestType import RequestType
from MetaDataApi.dataproviders.models.SerializableModel import SerializableModel


class Endpoint(models.Model, SerializableModel):
    endpoint_name = models.TextField()
    endpoint_url = models.TextField()
    request_type = models.TextField(choices=RequestType.build_choices(), default=RequestType.GET.value)
    data_provider = models.ForeignKey(DataProvider, related_name="endpoints", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data_provider} - {self.endpoint_name} - {self.endpoint_url}"

    def get_internal_view_url(self):
        return reverse('endpoint_detail', args=[str(self.data_provider.provider_name), self.endpoint_name])
