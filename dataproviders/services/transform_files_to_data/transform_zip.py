from django.conf import settings
from django.core.files.base import ContentFile

from MetaDataApi.utils.django_utils.django_file_utils import unzip_django_zipfile, FileType
from MetaDataApi.utils.json_utils.json_utils import JsonTypeInstance
from dataproviders.services.transform_files_to_data.base_transform_files_to_data import BaseTransformFilesToData
from dataproviders.services.transform_files_to_data.transform_methods import infer_object_name_from_path


class TransformZipMixin(BaseTransformFilesToData):
    def __init__(self):
        super().__init__()
        self.GET_DATA_FROM_FILE_OF_TYPE[FileType.ZIP] = self.get_data_from_zipfile

    def get_data_from_zipfile(self, file: ContentFile, origin_name):
        data = {}
        zip_file_object_name = self.infer_cleaned_object_name_from_file_name(file)
        for inner_zip_file_name, in_zip_file_content in unzip_django_zipfile(file).items():
            file_data = self.get_inner_zip_file_data(in_zip_file_content)
            if isinstance(file_data, JsonTypeInstance):
                self.add_file_data(data, file_data, inner_zip_file_name, origin_name, zip_file_object_name)
        return data

    def add_file_data(self, data, file_data, inner_zip_file_name, origin_name, zip_file_object_name):
        file_object_name = infer_object_name_from_path(inner_zip_file_name)
        object_name = self.join_object_names((origin_name, zip_file_object_name, file_object_name))
        if object_name in data.keys():
            self.add_file_data_as_list(file_data, object_name, data)
        else:
            data.update({object_name: file_data})

    def join_object_names(self, object_names):
        return "_".join([name for name in object_names if name])

    def add_file_data_as_list(self, file_data, object_name, data):
        if not isinstance(data[object_name], list):
            data[object_name] = [data[object_name], ]
        data[object_name].append(file_data)

    def get_inner_zip_file_data(self, in_zip_file_content):
        file_data = self.get_data_from_file_of_type(in_zip_file_content, origin_name=None)
        return file_data

    def infer_cleaned_object_name_from_file_name(self, file):
        cleaned_file_path = file.name.replace(settings.DATAFILE_STORAGE_PATH, "")
        zip_file_object_name = infer_object_name_from_path(cleaned_file_path)
        return zip_file_object_name
