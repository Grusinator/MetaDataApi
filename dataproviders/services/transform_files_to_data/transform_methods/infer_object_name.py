import os

from django.conf import settings

from dataproviders.services.transform_files_to_data.transform_methods.regex_patterns import REPattern


def infer_object_name_from_path(path: str):
    path = path.replace(settings.DATAFILE_STORAGE_PATH, "")
    path = convert_path_to_underscore_name(path)
    path = remove_id_like_strings(path)
    path = path.replace("-", "_")
    path = path.replace(".", "_")
    path = REPattern.multiple_underscore.replace("_", path)
    path = REPattern.trailing_underscore.remove(path)
    return path


def convert_path_to_underscore_name(path: str):
    path = os.path.splitext(path)[0]
    path = os.path.normpath(path)
    path = path.replace(os.sep, "_")
    return path


def remove_id_like_strings(string):
    string = REPattern.guid.remove(string)
    string = REPattern.guid_like.remove(string)
    string = REPattern.long_id.remove(string)
    return string
