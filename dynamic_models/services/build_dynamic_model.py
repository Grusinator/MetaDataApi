import logging

from json2model.services.dynamic_model import DynamicDataInstances, DynamicModelBuilder

from dataproviders.models.DataFile import DataFile
from dynamic_models.models.dynamic_meta_object import DynamicMetaObject

logger = logging.getLogger(__name__)


def build_models_from_provider_data_files(**data_file_filter):
    data_files = DataFile.objects.filter(**data_file_filter)
    for data_file in data_files:
        _try_build_model_from_data_file(data_file)


def build_meta_objects(built_objects, data_file):
    for obj in built_objects:
        DynamicMetaObject.objects.create(dynamic_model=obj, data_provider=data_file.data_provider)


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
        logger.info(f"Model building finished with {len(modelbuilder.built_objects)} objects created and "
                    f" {len(modelbuilder.failed_objects)} failed")
        build_meta_objects(modelbuilder.built_objects, data_file)


def load_data_from_provider_data_files(**data_file_filter):
    data_files = DataFile.objects.filter(**data_file_filter)
    for data_file in data_files:
        _try_load_data_from_data_file(data_file)


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
        logger.info(f"root label was not found in label info, in DataFile object: {data_file}")
        return None
