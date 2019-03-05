from django.core.exceptions import (
    ObjectDoesNotExist, MultipleObjectsReturned)


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

    @staticmethod
    def save_object(object, logger=None):

        try:
            object.save()
        except Exception as e:
            logger.error(str(e))
