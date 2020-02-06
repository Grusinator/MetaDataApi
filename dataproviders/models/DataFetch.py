from django.db import models
from django.urls import reverse
from jsonfield.fields import JSONField

from dataproviders.models.DataFileSourceBase import DataFileSourceBase
from dataproviders.models.Endpoint import Endpoint

data_fetch_on_save_methods = []


class DataFetch(DataFileSourceBase):
    endpoint = models.ForeignKey(Endpoint, related_name="data_fetches", on_delete=models.CASCADE)
    parameters = JSONField(null=True, blank=True)

    class Meta(DataFileSourceBase.Meta):
        default_related_name = '%(model_name)s'

    def __str__(self):
        return f"{self.date_created} - {self.endpoint} - {self.data_file_from_source}"

    def get_internal_view_url(self):
        return reverse('data_fetch_detail', args=[str(self.data_file_from_source).split("/")[1]])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.execute_on_save_methods()

    def execute_on_save_methods(self):
        for method in data_fetch_on_save_methods:
            method(self)
