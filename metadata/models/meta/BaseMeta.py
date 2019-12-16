import logging
from abc import abstractmethod, ABCMeta

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models

logger = logging.getLogger(__name__)


class BaseMeta(models.Model):
    __metaclass__ = ABCMeta

    label = models.TextField()
    description = models.TextField(null=True, blank=True)

    @staticmethod
    def get_schema_item(obj_type, raise_error=False, **search_kwargs):
        try:
            return obj_type.objects.get(**search_kwargs)
        except ObjectDoesNotExist as e:
            logger.error(str(e))
            if raise_error:
                raise e
            return None
        except MultipleObjectsReturned as e:
            logger.error(str(e))
            print("Warning: found multiple where it should not")
            if raise_error:
                raise e
            return obj_type.objects.filter(**search_kwargs).first()

    class Meta:
        abstract = True
        app_label = 'metadata'

    @abstractmethod
    def exists_by_label(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def exists(self, obj):
        raise NotImplementedError

    def create_if_not_exists(self):
        item_found = self.exists(self)
        if not item_found:
            self.save()
            return self
        else:
            return item_found

    @classmethod
    def get_all_labels(cls, **kwargs):
        schema_nodes = cls.objects.filter(**kwargs)
        return [obj.label for obj in schema_nodes]
