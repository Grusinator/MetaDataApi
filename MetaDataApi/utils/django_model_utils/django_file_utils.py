import os
import uuid
from enum import Enum
from zipfile import ZipFile

from django.core.files.base import ContentFile, File

from MetaDataApi.utils.django_model_utils.in_memory_zip_file import InMemoryZip


class FileType(Enum):
    TXT = ".txt"
    JSON = ".json"
    CSV = ".csv"
    ZIP = ".zip"


file_encoding = "utf-8"


def convert_file_to_str(file: ContentFile) -> str:
    return file.read().decode(file_encoding)


def create_django_file_from_local(file_path: str) -> File:
    local_file = open(file_path, "rb")
    file_name = get_default_file_name() + get_file_type(file_path).value
    return File(local_file, name=file_name)


def convert_binary_to_file(binary: bin, filename: str = None, filetype: FileType = FileType.TXT) -> ContentFile:
    filename = filename or get_default_file_name()
    filename += filetype.value
    file = ContentFile(binary, name=filename)
    return file


def convert_str_to_file(text_str: str, filename: str = None, filetype: FileType = FileType.TXT) -> ContentFile:
    binary = text_str.encode("utf-8")
    return convert_binary_to_file(binary, filename, filetype)


def create_django_zip_file(files: dict):
    imz = InMemoryZip()
    [imz.append(file_name, file_content) for file_name, file_content in files.items()]
    return convert_binary_to_file(imz.read_binary(), filetype=FileType.ZIP)


def unzip_django_zipfile(content_file: ContentFile):
    data_file_structure = {}
    content_file = File(content_file)  # The zipfile reader cant handle ContentFiles
    with ZipFile(content_file.file, 'r') as zf:
        for in_zip_file_name in zf.namelist():
            binary = zf.read(in_zip_file_name)
            data_file_structure[in_zip_file_name] = convert_binary_to_file(binary)
    return data_file_structure


def get_file_type(filename):
    return FileType(os.path.splitext(filename)[1])


def get_default_file_name() -> str:
    return str(uuid.uuid4())
