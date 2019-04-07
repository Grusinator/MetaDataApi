import logging

from django.core.exceptions import (
    ObjectDoesNotExist, MultipleObjectsReturned)

logger = logging.getLogger(__name__)


class DjangoModelUtils:

    @staticmethod
    def get_object_or_none(obj_type, **kwargs):
        try:
            return obj_type.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            print("Warning: found multiple where it should not")
            return obj_type.objects.filter(**kwargs).first()
