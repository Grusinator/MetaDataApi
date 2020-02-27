from django.core.files.base import ContentFile

from MetaDataApi.utils.django_utils.django_file_utils import unzip_django_zipfile, FileType
from MetaDataApi.utils.json_utils.json_utils import JsonTypeInstance
from dataproviders.services.transform_files_to_data import transform_methods
from dataproviders.services.transform_files_to_data.base_transform_files_to_data import BaseTransformFilesToData


class TransformZipMixin(BaseTransformFilesToData):
    def __init__(self):
        super().__init__()
        self.GET_DATA_FROM_FILE_OF_TYPE[FileType.ZIP] = self.get_data_from_zipfile

    def get_data_from_zipfile(self, file: ContentFile):
        data = {}
        zip_file_object_name = transform_methods.infer_object_name_from_path(file.name)
        for inner_zip_file_name, in_zip_file_content in unzip_django_zipfile(file).items():
            file_data = self.get_data_from_file_of_type(in_zip_file_content)
            if isinstance(file_data, JsonTypeInstance):
                object_name = self.build_inner_zip_object_name(zip_file_object_name, inner_zip_file_name)
                self.add_file_data(data, file_data, object_name)
        return data

    def add_file_data(self, data, file_data, object_name):
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

    def build_inner_zip_object_name(self, zip_file_object_name, inner_zip_file_name):
        file_object_name = transform_methods.infer_object_name_from_path(inner_zip_file_name)
        object_name = self.join_object_names((zip_file_object_name, file_object_name))
        return object_name
