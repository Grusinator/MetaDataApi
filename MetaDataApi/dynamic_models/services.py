import json
import logging

from json2model.services import dynamic_model

from MetaDataApi.dataproviders.models import DataDump

logger = logging.getLogger(__name__)


def load_data_from_provider_dumps(**filter):
    data_dumps = DataDump.objects.filter(**filter)
    for data_dump in data_dumps:
        data = json.loads(data_dump.file.read())
        root_name = data_dump.endpoint.endpoint_name
        try:
            dynamic_model.create_objects_from_json(root_name, data)
            dynamic_model.create_instances_from_json(root_name, data)
        except Exception as e:
            logger.warning(e)
