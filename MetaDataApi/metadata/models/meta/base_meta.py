import logging

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models

logger = logging.getLogger(__name__)


class BaseMeta(models.Model):
    label = models.TextField()
    description = models.TextField(null=True, blank=True)

    @staticmethod
    def get_schema_item(obj_type, **search_kwargs):
        try:
            return obj_type.objects.get(**search_kwargs)
        except ObjectDoesNotExist as e:
            logger.error(str(e))
            return None
        except MultipleObjectsReturned as e:
            logger.error(str(e))
            print("Warning: found multiple where it should not")
            return obj_type.objects.filter(**search_kwargs).first()

    class Meta:
        abstract = True
        app_label = 'metadata'
