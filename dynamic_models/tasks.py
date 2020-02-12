import logging

import celery
from celery import chain

import dynamic_models.services as data_loader_service
from dataproviders.models.DataFile import DataFile

logger = logging.getLogger(__name__)


@celery.shared_task
def build_models_from_data_files(**data_file_filter):
    return data_loader_service.build_models_from_provider_data_files(**data_file_filter)


@celery.shared_task
def load_data_from_data_files(**data_file_filter):
    return data_loader_service.load_data_from_provider_data_files(**data_file_filter)


def run_task_build_models_and_load_data_chained(data_file: DataFile):
    build_signature = build_models_from_data_files.si(pk=data_file.pk)
    load_signature = load_data_from_data_files.si(pk=data_file.pk)
    return chain(build_signature, load_signature).apply_async()
