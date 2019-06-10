import logging
import uuid
from enum import Enum

from django.core.exceptions import (
    ObjectDoesNotExist, MultipleObjectsReturned)
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


class DjangoModelUtils:

    @staticmethod
    def update(obj, data):
        obj.__dict__.update(data)
        obj.save()

    @staticmethod
    def get_object_or_none(obj_type, **kwargs):
        try:
            return obj_type.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            print("Warning: found multiple where it should not")
            return obj_type.objects.filter(**kwargs).first()

    class FileType(Enum):
        TXT = ".txt"
        JSON = ".json"
        CSV = ".csv"

    @classmethod
    def get_default_file_name(cls) -> str:
        return str(uuid.uuid4())

    @staticmethod
    def convert_file_to_str(file: ContentFile) -> str:
        return file.read().decode("utf-8")

    @classmethod
    def convert_str_to_file(cls, text_str: str, filename: str = None,
                            filetype: FileType = FileType.TXT) -> ContentFile:
        filename = filename or cls.get_default_file_name()
        filename += filetype.value
        text_str = text_str.encode("utf-8")
        file = ContentFile(text_str, name=filename)
        return file
