from django.db import models
from mutant.models import ModelDefinition

from dataproviders.models import DataProvider


class DynamicMetaObject(models.Model):
    dynamic_model = models.OneToOneField(ModelDefinition, related_name="meta_object", on_delete=models.CASCADE)
    data_provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data_provider} - {self.dynamic_model}"

    class Meta:
        default_related_name = "dynamic_meta_objects"
