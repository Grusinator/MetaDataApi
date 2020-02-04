import uuid
from enum import Enum

from django.core.files.base import ContentFile


class FileType(Enum):
    TXT = ".txt"
    JSON = ".json"
    CSV = ".csv"
    ZIP = ".zip"


def convert_file_to_str(file: ContentFile) -> str:
    return file.read().decode("utf-8")


def convert_str_to_file(text_str: str, filename: str = None, filetype: FileType = FileType.TXT) -> ContentFile:
    filename = filename or get_default_file_name()
    filename += filetype.value
    text_str = text_str.encode("utf-8")
    file = ContentFile(text_str, name=filename)
    return file


def create_zip_file(files: list):
    raise NotImplementedError


def get_default_file_name() -> str:
    return str(uuid.uuid4())
