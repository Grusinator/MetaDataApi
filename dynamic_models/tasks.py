import logging

import celery

import dynamic_models.services as data_loader_service

logger = logging.getLogger(__name__)


@celery.task
def build_models_from_provider_dumps(**dump_filter):
    return data_loader_service.build_models_from_provider_dumps(**dump_filter)


@celery.task
def build_models_from_data_dump(data_dump_pk):
    return data_loader_service.build_models_from_data_dump(data_dump_pk)


@celery.task
def load_data_from_provider_dumps(**dump_filter):
    return data_loader_service.load_data_from_provider_dumps(**dump_filter)


@celery.task
def load_data_from_data_dump(data_dump_pk):
    return data_loader_service.load_data_from_data_dump(data_dump_pk)
