import csv
import io
import logging

from django.core.files import File
from django.core.files.base import ContentFile

from MetaDataApi.utils import JsonUtils
from MetaDataApi.utils.django_model_utils.django_file_utils import FileType, get_file_type, unzip_django_zipfile, \
    convert_file_to_str

logger = logging.getLogger(__name__)


def handle_zipfile(file: ContentFile):
    data = {}
    file_dict = unzip_django_zipfile(file)
    for key, value in file_dict.items():
        filetype = get_file_type(file.name)
        handle_file_type_method = DATA_FROM_FILETYPE_METHOD_SELECTOR.get(filetype)
        file_data = handle_file_type_method(value)
        data.update(file_data)
    return data


def handle_json(file: ContentFile) -> str:
    return JsonUtils.clean(convert_file_to_str(file))


def handle_csv(file: ContentFile) -> str:
    with io.TextIOWrapper(file.file, encoding='utf-8') as text_file:
        reader = csv.DictReader(text_file)
        data = [row for row in reader]
        return JsonUtils.dumps(data)


def handle_txt(file: ContentFile):
    raise NotImplementedError


DATA_FROM_FILETYPE_METHOD_SELECTOR = {
    FileType.JSON: handle_json,
    FileType.CSV: handle_csv,
    FileType.TXT: handle_txt,
    FileType.ZIP: handle_zipfile,
}


def transform_data_file(file: File):
    filetype = get_file_type(file.name)
    get_data_from_filetype_method = DATA_FROM_FILETYPE_METHOD_SELECTOR.get(filetype)
    data = get_data_from_filetype_method(file)
    return data
