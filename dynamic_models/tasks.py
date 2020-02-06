import logging
from typing import Union

import celery
from celery import chain

import dynamic_models.services as data_loader_service
from dataproviders.admin import DataFetchAdmin, DataFileAdmin, DataFileUploadAdmin
from dataproviders.models.DataFetch import data_fetch_on_save_methods, DataFetch
from dataproviders.models.DataFile import data_file_on_save_methods
from dataproviders.models.DataFileUpload import data_file_upload_on_save_methods, DataFileUpload
from dataproviders.services import transform_files_to_data

logger = logging.getLogger(__name__)


@celery.shared_task
def build_models_from_data_files(**data_file_filter):
    return data_loader_service.build_models_from_provider_data_files(**data_file_filter)


# TODO refactor: dont have 2 methods here. just add data_file_pk=xx as arg
@celery.shared_task
def build_models_from_data_file(data_file_pk):
    return data_loader_service.build_models_from_data_file(data_file_pk)


@celery.shared_task
def load_data_from_data_files(**data_file_filter):
    return data_loader_service.load_data_from_provider_data_files(**data_file_filter)


@celery.shared_task
def load_data_from_data_file(data_file_pk):
    return data_loader_service.load_data_from_data_file(data_file_pk)


def run_task_build_models_and_load_data_chained(data_fetch: DataFetch):
    build_signature = build_models_from_data_file.si(data_fetch.pk)
    load_signature = load_data_from_data_file.si(data_fetch.pk)
    return chain(build_signature, load_signature).apply_async()


@celery.shared_task
def clean_data_from_source(data_file_upload_pk, is_from_file_upload: bool):
    DataObjectClass = DataFileUpload if is_from_file_upload else DataFetch
    data_file_source = DataObjectClass.objects.get(pk=data_file_upload_pk)
    data = transform_files_to_data.clean_data_from_data_file(data_file_source.data_file_from_source.file)
    transform_files_to_data.create_data_file(data, data_file_source.user, data_file_source)


def run_task_clean_data_from_source_file(data_object: Union[DataFileUpload, DataFetch]):
    is_from_file_upload = isinstance(data_object, DataFileUpload)
    clean_data_from_source.delay(data_object.pk, is_from_file_upload)


def connect_tasks():
    data_file_on_save_methods.append(run_task_build_models_and_load_data_chained)
    DataFileAdmin.add_action_from_single_arg_method(run_task_build_models_and_load_data_chained)

    data_file_upload_on_save_methods.append(run_task_clean_data_from_source_file)
    DataFileUploadAdmin.add_action_from_single_arg_method(run_task_clean_data_from_source_file)

    data_fetch_on_save_methods.append(run_task_clean_data_from_source_file)
    DataFetchAdmin.add_action_from_single_arg_method(run_task_clean_data_from_source_file)
