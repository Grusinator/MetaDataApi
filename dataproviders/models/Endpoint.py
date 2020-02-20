from django.db import models
from django.urls import reverse
from generic_serializer import SerializableModel

from dataproviders.models.ApiTypes import ApiTypes
from dataproviders.models.DataProvider import DataProvider
from dataproviders.models.RequestType import RequestType


class Endpoint(models.Model, SerializableModel):
    endpoint_name = models.TextField()
    endpoint_url = models.TextField()
    request_type = models.CharField(choices=RequestType.build_choices(), default=RequestType.GET.value, max_length=10)
    api_type = models.CharField(choices=ApiTypes.build_choices(), default=ApiTypes.OAUTH_REST.value, max_length=15)
    data_provider = models.ForeignKey(DataProvider, related_name="endpoints", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data_provider} - {self.endpoint_name} - {self.endpoint_url}"

    def get_internal_view_url(self):
        return reverse('endpoint_detail', args=[str(self.data_provider.provider_name), self.endpoint_name])
