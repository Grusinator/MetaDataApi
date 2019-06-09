from django.db import models

from MetaDataApi.dataproviders.models.DataProvider import DataProvider


class Endpoint(models.Model):
    endpoint_name = models.TextField()
    endpoint_url = models.TextField()
    provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.provider} - {self.endpoint_name} - {self.endpoint_url}"
