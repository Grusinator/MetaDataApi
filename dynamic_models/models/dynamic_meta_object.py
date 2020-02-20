from django.db import models
from mutant.models import ModelDefinition

from dataproviders.models import DataProvider


class DynamicMetaObject(models.Model):
    dynamic_model = models.OneToOneField(ModelDefinition, on_delete=models.CASCADE)
    data_provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "dynamic_meta_objects"
