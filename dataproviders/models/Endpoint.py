from django.db import models
from django.urls import reverse
from generic_serializer import SerializableModel

from dataproviders.models.ApiType import ApiType
from dataproviders.models.AuthType import AuthType
from dataproviders.models.DataProvider import DataProvider
from dataproviders.models.RequestType import RequestType


class Endpoint(models.Model, SerializableModel):
    endpoint_name = models.TextField(max_length=50)
    endpoint_url = models.TextField()
    requires_auth = models.BooleanField(default=False)
    request_type = models.CharField(choices=RequestType.build_choices(), default=RequestType.GET.value, max_length=10)
    api_type = models.CharField(choices=ApiType.build_choices(), default=ApiType.REST.value, max_length=10)
    auth_type = models.CharField(choices=AuthType.build_choices(), default=AuthType.NONE.value, null=True, blank=True,
                                 max_length=10)
    data_provider = models.ForeignKey(DataProvider, related_name="endpoints", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data_provider} - {self.endpoint_name} - {self.endpoint_url}"

    def get_internal_view_url(self):
        return reverse('endpoint_detail', args=[str(self.data_provider.provider_name), self.endpoint_name])
