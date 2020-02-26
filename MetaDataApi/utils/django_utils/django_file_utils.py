import os
import uuid
from enum import Enum
from typing import Union
from zipfile import ZipFile

from django.core.files.base import ContentFile, File

from MetaDataApi.utils.django_utils.in_memory_zip_file import InMemoryZip


class FileType(Enum):
    TXT = ".txt"
    JSON = ".json"
    CSV = ".csv"
    ZIP = ".zip"
    # IMAGE = ".jpg"
    UNKNOWN = ""

    @classmethod
    def identify(cls, filename: str, default_to_unknown=True):
        ext = os.path.splitext(filename)[1]
        try:
            return FileType(ext)
        except ValueError:
            return cls.UNKNOWN if default_to_unknown else ext


file_encoding = "utf-8"


def convert_file_to_str(file: ContentFile) -> str:
    return file.read().decode(file_encoding)


def create_django_file_from_local(file_path: str) -> File:
    local_file = open(file_path, "rb")
    file_name = get_default_file_name(based_on=file_path)
    return File(local_file, name=file_name)


def convert_binary_to_file(binary: bin, filename_based_on: str = None,
                           force_ext: Union[FileType, str] = None) -> ContentFile:
    filename = get_default_file_name(based_on=filename_based_on, force_ext=force_ext)
    file = ContentFile(binary, name=filename)
    return file


def convert_str_to_file(text_str: str, filename_based_on: str = None, filetype: FileType = None) -> ContentFile:
    binary = text_str.encode(file_encoding)
    return convert_binary_to_file(binary, filename_based_on, filetype)


def create_django_zip_file(files: dict):
    imz = InMemoryZip()
    [imz.append(file_name, file_content) for file_name, file_content in files.items()]
    return convert_binary_to_file(imz.read_binary(), force_ext=FileType.ZIP)


def unzip_django_zipfile(content_file: ContentFile):
    data_file_structure = {}
    content_file = File(content_file)  # The zipfile reader cant handle ContentFiles
    with ZipFile(content_file.file, 'r') as zf:
        for in_zip_file_name in zf.namelist():
            binary = zf.read(in_zip_file_name)
            ext = FileType.identify(in_zip_file_name, default_to_unknown=False)
            data_file_structure[in_zip_file_name] = convert_binary_to_file(binary, filename_based_on=in_zip_file_name,
                                                                           force_ext=ext)
    return data_file_structure


def get_filename(path):
    basename = os.path.basename(path)
    return os.path.splitext(basename)[0]


def get_file_ext(path):
    return os.path.splitext(path)[1]


def get_default_file_name(based_on=None, force_ext: Union[FileType, str] = None) -> str:
    base_name = str(uuid.uuid4())
    # TODO identify and remove guids before adding
    if based_on:
        base_name += "-" + get_filename(based_on)
    if force_ext:
        base_name += force_ext.value if isinstance(force_ext, FileType) else force_ext
    elif based_on:
        base_name += FileType.identify(based_on).value
    else:
        base_name += FileType.TXT.value
    return base_name
