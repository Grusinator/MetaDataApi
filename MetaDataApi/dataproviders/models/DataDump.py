from django.db import models

from MetaDataApi.dataproviders.models.Endpoint import Endpoint


class DataDump(models.Model):
    date_downloaded = models.DateField()
    endpoint = models.ForeignKey(Endpoint, related_name="data_dumps", on_delete=models.CASCADE)
    data = models.FileField()

    def __str__(self):
        return f"{self.date_downloaded} - {self.endpoint} - {self.data}"
