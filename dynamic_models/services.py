import json
import logging

from json2model.services.dynamic_model import DynamicDataInstances, DynamicModelBuilder

from dataproviders.models import DataDump

logger = logging.getLogger(__name__)


def build_models_from_provider_dumps(**dump_filter):
    data_dumps = DataDump.objects.filter(**dump_filter)
    for data_dump in data_dumps:
        _try_build_model_from_data_dump(data_dump)


def build_models_from_data_dump(data_dump_pk: int):
    data_dump = DataDump.objects.get(pk=data_dump_pk)
    _try_build_model_from_data_dump(data_dump)


def _try_build_model_from_data_dump(data_dump):
    data = json.loads(data_dump.file.read())
    root_name = data_dump.endpoint.endpoint_name
    modelbuilder = DynamicModelBuilder()
    try:
        modelbuilder.create_models_from_data(root_name, data)
    except Exception as e:
        logger.warning(e)


def load_data_from_provider_dumps(**dump_filter):
    data_dumps = DataDump.objects.filter(**dump_filter)
    for data_dump in data_dumps:
        _try_load_data_from_data_dump(data_dump)


def load_data_from_data_dump(data_dump_pk: int):
    data_dump = DataDump.objects.get(pk=data_dump_pk)
    return _try_load_data_from_data_dump(data_dump)


def _try_load_data_from_data_dump(data_dump):
    data = json.loads(data_dump.file.read())
    root_name = data_dump.endpoint.endpoint_name
    data_builder = DynamicDataInstances()
    try:
        data_builder.create_instances_from_data(root_name, data)
    except Exception as e:
        logger.warning(e)
