# Create your tasks here
from __future__ import absolute_import, unicode_literals

import celery
from django.contrib.auth.models import User

import dataproviders.services.fetch_data_from_provider as fetch_service
from dataproviders.models import DataProviderUser


@celery.shared_task
def fetch_data_for_each_user():
    for user in User.objects.all():
        fetch_data_related_to_user(user.id)


@celery.shared_task
def fetch_data_related_to_user(user_pk):
    data_provider_users = DataProviderUser.objects.filter(user_id=user_pk)
    for data_provider_user in data_provider_users:
        if data_provider_user.data_fetching_is_active:
            fetch_data_from_provider_related_to_user(data_provider_user.pk)


@celery.shared_task
def fetch_data_from_provider_related_to_user(data_provider_user_pk):
    data_provider_user = DataProviderUser.objects.get(pk=data_provider_user_pk)
    for endpoint in data_provider_user.data_provider.endpoints.all():
        fetch_data_from_endpoint.delay(
            data_provider_user.data_provider.provider_name,
            endpoint.endpoint_name,
            data_provider_user.user.pk
        )


@celery.shared_task
def fetch_data_from_endpoint(provider_name, endpoint_name, user_pk):
    return fetch_service.fetch_data_from_endpoint(provider_name, endpoint_name, user_pk)
