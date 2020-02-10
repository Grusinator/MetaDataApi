import logging

import celery
from celery import chain

import dynamic_models.services as data_loader_service
from dataproviders.models.DataFetch import DataFetch

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



