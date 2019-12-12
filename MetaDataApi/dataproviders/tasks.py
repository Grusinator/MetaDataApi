# Create your tasks here
from __future__ import absolute_import, unicode_literals

import celery

import MetaDataApi.dataproviders.services.fetch_data_from_provider as fetch_service


@celery.shared_task
def add(x, y):
    return x + y


@celery.shared_task()
def fetch_all():
    fetch_data_from_provider_endpoint


@celery.shared_task
def fetch_data_from_provider_endpoint(provider_name, endpoint_name, user_pk):
    return fetch_service.fetch_data_from_provider_endpoint(provider_name, endpoint_name, user_pk)
