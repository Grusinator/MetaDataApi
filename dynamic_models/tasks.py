import logging

import celery
from celery import chain

import dynamic_models.services as data_loader_service
from dataproviders.models.DataDump import data_dump_save_methods, DataDump

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


def build_models_and_load_data_chained(data_dump: DataDump):
    build_signature = build_models_from_data_dump.si(data_dump.pk)
    load_signature = load_data_from_data_dump.si(data_dump.pk)
    return chain(build_signature, load_signature).apply_async()


def build_models(data_dump: DataDump):
    return build_models_from_data_dump.delay(data_dump.pk)


# add the task to be executed when dumps are saved, maybe not the best solution.
data_dump_save_methods.append(build_models)
data_dump_save_methods.append(build_models_and_load_data_chained)
