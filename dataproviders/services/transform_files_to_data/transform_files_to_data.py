import logging

from django.core.files.base import ContentFile

from MetaDataApi.utils import JsonUtils, JsonType
from MetaDataApi.utils.django_utils.django_file_utils import FileType, convert_file_to_str
from dataproviders.services.transform_files_to_data.transform_csv import TransformCsvMixin
from dataproviders.services.transform_files_to_data.transform_zip import TransformZipMixin

logger = logging.getLogger(__name__)


class TransformFilesToData(TransformZipMixin, TransformCsvMixin):
    def __init__(self):
        super().__init__()
        self.GET_DATA_FROM_FILE_OF_TYPE[FileType.JSON] = self.get_data_from_json_file

    def get_data_from_json_file(self, file: ContentFile) -> JsonType:
        data = convert_file_to_str(file)
        return JsonUtils.validate(data)
