import csv
import io
import logging

from django.core.files.base import ContentFile
from json2model.services.data_type_transform import transform_data_type

from MetaDataApi.utils import JsonType, JsonUtils
from MetaDataApi.utils.django_utils.django_file_utils import FileType
from dataproviders.services.transform_files_to_data.base_transform_files_to_data import BaseTransformFilesToData

logger = logging.getLogger(__name__)


class TransformCsvMixin(BaseTransformFilesToData):
    def __init__(self):
        super().__init__()
        self.GET_DATA_FROM_FILE_OF_TYPE[FileType.CSV] = self.get_data_from_csv_file

    def get_data_from_csv_file(self, file: ContentFile, origin_name=None) -> JsonType:
        with io.TextIOWrapper(file, encoding="utf-8") as text_file:
            dialect = self.get_csv_dialect(text_file)
            csv_start = self.read_csv_start_of_file(text_file, dialect)
            fieldnames, data_start_line_nr = self.get_or_create_fieldnames(csv_start)
            data = self.get_data_from_csv(text_file, dialect, fieldnames, data_start_line_nr)
            return JsonUtils.validate(data)

    def get_csv_dialect(self, text_file):
        text_file.seek(0)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(text_file.read(200), delimiters=",;")
        except Exception:
            logger.warning("csv dialect was not found")
            return None
        else:
            text_file.seek(0)
        return dialect

    def read_csv_start_of_file(self, text_file, dialect):
        text_file.seek(0)
        reader = csv.reader(text_file, dialect=dialect)
        return [row for n, row in enumerate(reader) if n < 50]

    def get_or_create_fieldnames(self, rows):
        for n, row in enumerate(rows):
            transformed_row = [transform_data_type(cell) for cell in row]
            is_header = all(isinstance(cell, str) for cell in transformed_row)
            if is_header:
                return row, n + 1
            elif n > 10:
                return self.build_fieldnames(transformed_row), 0

    def get_data_from_csv(self, text_file, dialect, fieldnames, data_start_line_nr):
        text_file.seek(0)
        reader = csv.DictReader(text_file, fieldnames=fieldnames, dialect=dialect)
        data = [row for row in reader]
        data = data[data_start_line_nr:]
        return data

    def build_fieldnames(self, transformed_first_line):
        return [f"{type(cell).__name__}_col{n}" for n, cell in enumerate(transformed_first_line)]
