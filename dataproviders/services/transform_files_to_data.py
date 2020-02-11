import csv
import io
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from MetaDataApi.utils import JsonUtils, JsonType
from MetaDataApi.utils.django_model_utils import django_file_utils
from MetaDataApi.utils.django_model_utils.django_file_utils import FileType, get_file_type, unzip_django_zipfile, \
    convert_file_to_str
from dataproviders.models import DataFileUpload, DataFetch
from dataproviders.models.DataFile import DataFile
from dataproviders.models.DataFileSourceBase import DataFileSourceBase
from dataproviders.services.transform_methods import json_key_string_replace
from dataproviders.services.transform_methods.infer_object_name import infer_object_name_from_path

logger = logging.getLogger(__name__)


def add_file_data_as_list(file_data, object_name, data):
    if not isinstance(data[object_name], list):
        data[object_name] = [data[object_name], ]
    data[object_name].append(file_data)


def handle_zipfile(file: ContentFile):
    data = {}
    cleaned_file_path = file.name.replace(settings.DATAFILE_STORAGE_PATH, "")
    zip_file_object_name = infer_object_name_from_path(cleaned_file_path)
    file_dict = unzip_django_zipfile(file)
    for in_zip_file_name, in_zip_file_content in file_dict.items():
        file_type = get_file_type(in_zip_file_name)
        handle_file_type_method = DATA_FROM_FILETYPE_METHOD_SELECTOR.get(file_type)
        file_data = handle_file_type_method(in_zip_file_content)
        object_name = infer_object_name_from_path(in_zip_file_name)
        object_name = join_object_names((zip_file_object_name, object_name))
        if object_name in data.keys():
            add_file_data_as_list(file_data, object_name, data)
        else:
            data.update({object_name: file_data})
    return data


def join_object_names(object_names):
    return "_".join([name for name in object_names if name is not ""])


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


def clean_data(data):
    return json_key_string_replace.clean_invalid_key_chars(data)


def clean_data_from_data_file(file: ContentFile) -> JsonType:
    filetype = get_file_type(file.name)
    get_data_from_filetype_method = DATA_FROM_FILETYPE_METHOD_SELECTOR.get(filetype)
    data = get_data_from_filetype_method(file)
    cleaned_data = clean_data(data)
    return cleaned_data


def build_label_info_for_data_file_upload(data_file_source: DataFileUpload):
    return {"root_label": data_file_source.data_provider.provider_name}


def build_label_info_for_data_fetch(data_file_source: DataFetch):
    return {"root_label": data_file_source.endpoint.endpoint_name}


def create_data_file(data: JsonType, user: User, data_file_source: DataFileSourceBase, label_info=None):
    data_file = django_file_utils.convert_str_to_file(JsonUtils.dumps(data), filetype=FileType.JSON)
    label_info = label_info or build_label_info(data_file_source)
    data_file_object = DataFile.objects.create(data_file=data_file, user=user, label_info=label_info)
    update_source_object(data_file_object, data_file_source)
    return data_file_object


def build_label_info(data_file_source):
    if isinstance(data_file_source, DataFetch):
        return build_label_info_for_data_fetch(data_file_source)
    elif isinstance(data_file_source, DataFileUpload):
        return build_label_info_for_data_file_upload(data_file_source)


def update_source_object(data_file_object, data_file_source):
    data_file_source.refined_data_file = data_file_object
    data_file_source.has_been_refined = True
    data_file_source.save()
