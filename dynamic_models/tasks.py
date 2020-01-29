import logging

import celery
from celery import chain

import dynamic_models.services as data_loader_service
from dataproviders.admin import DataDumpAdmin
from dataproviders.models.data_dump import data_dump_save_methods, DataDump

logger = logging.getLogger(__name__)


@celery.shared_task
def build_models_from_provider_dumps(**dump_filter):
    return data_loader_service.build_models_from_provider_dumps(**dump_filter)


@celery.shared_task
def build_models_from_data_dump(data_dump_pk):
    return data_loader_service.build_models_from_data_dump(data_dump_pk)


@celery.shared_task
def load_data_from_provider_dumps(**dump_filter):
    return data_loader_service.load_data_from_provider_dumps(**dump_filter)


@celery.shared_task
def load_data_from_data_dump(data_dump_pk):
    return data_loader_service.load_data_from_data_dump(data_dump_pk)


def build_models_and_load_data_chained(data_dump: DataDump):
    build_signature = build_models_from_data_dump.si(data_dump.pk)
    load_signature = load_data_from_data_dump.si(data_dump.pk)
    return chain(build_signature, load_signature).apply_async()


def build_models(data_dump: DataDump):
    return build_models_from_data_dump.delay(data_dump.pk)


def connect_tasks():
    # add the task to be executed when dumps are saved, maybe not the best solution.
    # data_dump_save_methods.append(lambda data_dump: build_models_from_data_dump(data_dump.pk))
    # data_dump_save_methods.append(build_models)
    data_dump_save_methods.append(build_models_and_load_data_chained)
    DataDumpAdmin.add_action_from_single_arg_method(build_models_and_load_data_chained)
