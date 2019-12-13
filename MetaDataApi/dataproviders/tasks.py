# Create your tasks here
from __future__ import absolute_import, unicode_literals

import celery
from celery.schedules import crontab

import MetaDataApi.dataproviders.services.fetch_data_from_provider as fetch_service
from MetaDataApi.celery import app
from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.users.models import Profile


@celery.shared_task
def add(x, y):
    return x + y


@celery.shared_task
def fetch_data_from_provider_endpoint(provider_name, endpoint_name, user_pk):
    return fetch_service.fetch_data_from_provider_endpoint(provider_name, endpoint_name, user_pk)


@celery.shared_task
def fetch_all(user_pk):
    for provider in DataProvider.objects.all():
        for endpoint in provider.endpoints:
            fetch_data_from_provider_endpoint.delay(provider.provider_name, endpoint.endpoint_name, user_pk)


@celery.shared_task
def test_django_model():
    return Profile.objects.all().first()


app.conf.beat_schedule = {
    "nighly-data-update": {
        "task": "tasks.fetch_all",
        "schedule": crontab(hour=4, minute=0),
        'args': {"user_pk": 1}
    }
}
