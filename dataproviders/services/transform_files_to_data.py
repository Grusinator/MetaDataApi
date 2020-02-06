import csv
import io
import logging
import os

from django.core.files.base import ContentFile

from MetaDataApi.utils import JsonUtils, JsonType
from MetaDataApi.utils.django_model_utils.django_file_utils import FileType, get_file_type, unzip_django_zipfile, \
    convert_file_to_str

logger = logging.getLogger(__name__)


def infer_object_name_from_path(in_zip_file_name):
    filedir = os.path.splitext(in_zip_file_name)[0]
    return filedir


def handle_zipfile(file: ContentFile):
    data = {}
    file_dict = unzip_django_zipfile(file)
    for in_zip_file_name, in_zip_file_content in file_dict.items():
        filetype = get_file_type(in_zip_file_name)
        handle_file_type_method = DATA_FROM_FILETYPE_METHOD_SELECTOR.get(filetype)
        file_data = handle_file_type_method(in_zip_file_content)
        object_name = infer_object_name_from_path(in_zip_file_name)
        data.update({object_name: file_data})
    return data


def handle_json(file: ContentFile) -> JsonType:
    return JsonUtils.validate(convert_file_to_str(file))


def handle_csv(file: ContentFile) -> JsonType:
    with io.TextIOWrapper(file.file, encoding='utf-8') as text_file:
        reader = csv.DictReader(text_file)
        data = [row for row in reader]
        return JsonUtils.validate(data)


def handle_txt(file: ContentFile) -> JsonType:
    raise NotImplementedError


DATA_FROM_FILETYPE_METHOD_SELECTOR = {
    FileType.JSON: handle_json,
    FileType.CSV: handle_csv,
    FileType.TXT: handle_txt,
    FileType.ZIP: handle_zipfile,
}


def transform_data_file(file: ContentFile) -> JsonType:
    filetype = get_file_type(file.name)
    get_data_from_filetype_method = DATA_FROM_FILETYPE_METHOD_SELECTOR.get(filetype)
    data = get_data_from_filetype_method(file)
    return data
