# Create your tasks here
from __future__ import absolute_import, unicode_literals

import celery
from django.contrib.auth.models import User

import dataproviders.services.fetch_data_from_provider as fetch_service
from dataproviders.models import DataProviderUser


@celery.shared_task
def fetch_data_from_provider_endpoint(provider_name, endpoint_name, user_pk):
    return fetch_service.fetch_data_from_provider_endpoint(provider_name, endpoint_name, user_pk)


@celery.shared_task
def fetch_all_data_from_data_provider_user(user_pk):
    data_provider_users = DataProviderUser.objects.filter(user_id=user_pk)
    for data_provider_user in data_provider_users:
        if data_provider_user.data_fetching_is_active:
            fetch_data_from_all_provider_endpoints(data_provider_user, user_pk)


def fetch_data_from_all_provider_endpoints(data_provider_user, user_pk):
    for endpoint in data_provider_user.data_provider.endpoints.all():
        fetch_data_from_provider_endpoint.delay(
            data_provider_user.data_provider.provider_name,
            endpoint.endpoint_name,
            user_pk
        )


@celery.shared_task
def fetch_all_data_from_providers():
    for user in User.objects.all():
        fetch_all_data_from_data_provider_user.delay(user.id)
