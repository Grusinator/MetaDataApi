import logging

from json2model.services.dynamic_model import DynamicDataInstances, DynamicModelBuilder

from dataproviders.models.DataFile import DataFile

logger = logging.getLogger(__name__)


def build_models_from_provider_data_files(**data_file_filter):
    data_files = DataFile.objects.filter(**data_file_filter)
    for data_file in data_files:
        _try_build_model_from_data_file(data_file)


def build_models_from_data_file(data_file_pk: int):
    data_file = DataFile.objects.get(pk=data_file_pk)
    _try_build_model_from_data_file(data_file)


def _try_build_model_from_data_file(data_file: DataFile):
    data = data_file.read_data()
    root_label = get_root_label(data_file)
    modelbuilder = DynamicModelBuilder()
    try:
        modelbuilder.create_models_from_data(data, root_label)
    except Exception as e:
        logger.warning(e)
        raise e
    else:
        if modelbuilder.failed_objects:
            logger.warning(modelbuilder.failed_objects)


def load_data_from_provider_data_files(**data_file_filter):
    data_files = DataFile.objects.filter(**data_file_filter)
    for data_file in data_files:
        _try_load_data_from_data_file(data_file)


def load_data_from_data_file(data_file_pk: int):
    data_file = DataFile.objects.get(pk=data_file_pk)
    return _try_load_data_from_data_file(data_file)


def _try_load_data_from_data_file(data_file: DataFile):
    data = data_file.read_data()
    root_label = get_root_label(data_file)
    data_builder = DynamicDataInstances(user_pk=data_file.user.pk)
    try:
        data_builder.create_instances_from_data(data, root_label)
    except Exception as e:
        logger.warning(e)


def get_root_label(data_file: DataFile):
    try:
        return data_file.label_info["root_label"]
    except:
        logger.error(f"root label was not found in label info, in DataFile object: {data_file}")
        return None
