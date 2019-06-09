from django.db import models

from MetaDataApi.dataproviders.models.Endpoint import Endpoint


class DataDump(models.Model):
    date = models.DateField()
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    data = models.FileField()

    def __str__(self):
        return f"{self.date} - {self.endpoint} - {self.data}"
