import logging

from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from MetaDataApi.utils import JsonUtils, JsonType
from MetaDataApi.utils.django_utils import django_file_utils
from MetaDataApi.utils.django_utils.django_file_utils import FileType
from MetaDataApi.utils.json_utils.json_utils import JsonTypeInstance
from dataproviders.models import DataFileUpload, DataFetch
from dataproviders.models.DataFile import DataFile
from dataproviders.models.DataFileSourceBase import DataFileSourceBase
from dataproviders.services.transform_files_to_data import transform_methods

logger = logging.getLogger(__name__)


class BaseTransformFilesToData:
    GET_DATA_FROM_FILE_OF_TYPE = {}

    def _insert_origin_name(self, data, origin_name):
        if origin_name:
            return {origin_name: data}
        else:
            return data

    @classmethod
    def get_data_from_unknown_file(self, file: ContentFile, origin_name=None):
        logger.warning(f"this file type: {FileType.identify(file.name)} is not supported: {file.name}")

    def clean_data_from_data_file_source(self, data_file_source: DataFileSourceBase):
        data = self.clean_data_from_file(data_file_source.data_file_from_source.file)
        self.create_data_file(data, data_file_source.user, data_file_source)

    def clean_data_from_file(self, file: ContentFile) -> JsonType:
        origin_name = transform_methods.infer_object_name_from_path(file.name)
        data = self.get_data_from_file_of_type(file, origin_name)
        if FileType.identify(file.name) != FileType.ZIP:
            data = self._insert_origin_name(data, origin_name)
        cleaned_data = self.clean_data(data)
        return cleaned_data

    def get_data_from_file_of_type(self, file, origin_name):
        filetype = FileType.identify(file.name)
        get_data_from_filetype = self.GET_DATA_FROM_FILE_OF_TYPE.get(filetype, self.get_data_from_unknown_file)
        data = get_data_from_filetype(file, origin_name)
        return data

    def clean_data(self, data):
        if isinstance(data, JsonTypeInstance):
            return transform_methods.clean_key_value_strings(data)

    def create_data_file(self, data: JsonType, user: User, data_file_source: DataFileSourceBase, label_info=None):
        data_file = django_file_utils.convert_str_to_file(JsonUtils.dumps(data), filetype=FileType.JSON)
        # label_info = label_info or build_label_info(data_file_source)
        data_file_object = DataFile.objects.create(
            data_file=data_file, user=user, label_info=label_info, data_provider=data_file_source.data_provider)
        self._update_source_object(data_file_object, data_file_source)
        return data_file_object

    def _update_source_object(self, data_file_object, data_file_source):
        data_file_source.refined_data_file = data_file_object
        data_file_source.has_been_refined = True
        data_file_source.save()

    def build_label_info(self, data_file_source):
        if isinstance(data_file_source, DataFetch):
            return self.build_label_info_for_data_fetch(data_file_source)
        elif isinstance(data_file_source, DataFileUpload):
            return self.build_label_info_for_data_file_upload(data_file_source)

    def build_label_info_for_data_fetch(self, data_file_source: DataFetch):
        return {"root_label": data_file_source.endpoint.endpoint_name}

    def build_label_info_for_data_file_upload(self, data_file_source: DataFileUpload):
        return {"root_label": data_file_source.data_provider.provider_name}
