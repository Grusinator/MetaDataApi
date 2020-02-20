import csv
import io
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from MetaDataApi.utils import JsonUtils, JsonType
from MetaDataApi.utils.django_utils import django_file_utils
from MetaDataApi.utils.django_utils.django_file_utils import FileType, unzip_django_zipfile, convert_file_to_str
from MetaDataApi.utils.json_utils.json_utils import JsonTypeInstance
from dataproviders.models import DataFileUpload, DataFetch
from dataproviders.models.DataFile import DataFile
from dataproviders.models.DataFileSourceBase import DataFileSourceBase
from dataproviders.services.transform_methods import json_key_value_string_replace
from dataproviders.services.transform_methods.infer_object_name import infer_object_name_from_path

logger = logging.getLogger(__name__)


def add_file_data_as_list(file_data, object_name, data):
    if not isinstance(data[object_name], list):
        data[object_name] = [data[object_name], ]
    data[object_name].append(file_data)


def get_data_from_zipfile(file: ContentFile, origin_name):
    data = {}
    cleaned_file_path = file.name.replace(settings.DATAFILE_STORAGE_PATH, "")
    zip_file_object_name = infer_object_name_from_path(cleaned_file_path)
    for inner_zip_file_name, in_zip_file_content in unzip_django_zipfile(file).items():
        file_data = get_inner_zip_file_data(inner_zip_file_name, in_zip_file_content)
        if isinstance(file_data, JsonTypeInstance):
            add_file_data(data, file_data, inner_zip_file_name, origin_name, zip_file_object_name)
    return data


def add_file_data(data, file_data, inner_zip_file_name, origin_name, zip_file_object_name):
    file_object_name = infer_object_name_from_path(inner_zip_file_name)
    object_name = join_object_names((origin_name, zip_file_object_name, file_object_name))
    if object_name in data.keys():
        add_file_data_as_list(file_data, object_name, data)
    else:
        data.update({object_name: file_data})


def get_inner_zip_file_data(in_zip_file_name, in_zip_file_content):
    file_type = FileType.identify(in_zip_file_name)
    get_data_from_filetype = GET_DATA_FROM_FILETYPE_METHOD_SELECTOR.get(file_type)
    file_data = get_data_from_filetype(
        in_zip_file_content,
        origin_name=None  # origin_name=None: The origin shall not be added in files further inside
    )
    return file_data


def join_object_names(object_names):
    return "_".join([name for name in object_names if name])


def get_data_from_json_file(file: ContentFile, origin_name) -> JsonType:
    data = convert_file_to_str(file)
    return validate_and_insert_origin_name(data, origin_name)


def get_data_from_csv_file(file: ContentFile, origin_name) -> JsonType:
    with io.TextIOWrapper(file.file, encoding='utf-8') as text_file:
        reader = csv.DictReader(text_file)
        data = [row for row in reader]
        return validate_and_insert_origin_name(data, origin_name)


def validate_and_insert_origin_name(data, origin_name):
    validated_data = JsonUtils.validate(data)
    if origin_name:
        return {origin_name: validated_data}
    else:
        return validated_data


def get_data_from_unknown_file(file: ContentFile, origin_name):
    logger.warning(f"this file type is not supported: {file.name}")


GET_DATA_FROM_FILETYPE_METHOD_SELECTOR = {
    FileType.JSON: get_data_from_json_file,
    FileType.CSV: get_data_from_csv_file,
    FileType.ZIP: get_data_from_zipfile,
    FileType.TXT: get_data_from_unknown_file,
    FileType.UNKNOWN: get_data_from_unknown_file
}


def clean_json_data(data):
    if isinstance(data, JsonTypeInstance):
        return json_key_value_string_replace.clean_key_value_strings(data)


def clean_data_from_data_file(file: ContentFile, origin_name=None) -> JsonType:
    filetype = FileType.identify(file.name)
    get_data_from_filetype = GET_DATA_FROM_FILETYPE_METHOD_SELECTOR.get(filetype)
    data = get_data_from_filetype(file, origin_name)
    cleaned_data = clean_json_data(data)
    return cleaned_data


def build_label_info_for_data_file_upload(data_file_source: DataFileUpload):
    return {"root_label": data_file_source.data_provider.provider_name}


def build_label_info_for_data_fetch(data_file_source: DataFetch):
    return {"root_label": data_file_source.endpoint.endpoint_name}


def create_data_file(data: JsonType, user: User, data_file_source: DataFileSourceBase, label_info=None):
    data_file = django_file_utils.convert_str_to_file(JsonUtils.dumps(data), filetype=FileType.JSON)
    label_info = label_info  # or build_label_info(data_file_source)
    data_file_object = DataFile.objects.create(
        data_file=data_file, user=user, label_info=label_info, data_provider=data_file_source.data_provider)
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
