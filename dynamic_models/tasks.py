import logging

import celery

import dynamic_models.services as data_loader_service

logger = logging.getLogger(__name__)


@celery.shared_task
def load_data_from_provider_dumps(**filter):
    return data_loader_service.build_models_from_provider_dumps(**filter)
