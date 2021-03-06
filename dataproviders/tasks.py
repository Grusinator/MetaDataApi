# Create your tasks here
from __future__ import absolute_import, unicode_literals

import celery
from django.contrib.auth.models import User

import dataproviders.services.fetch_data_from_provider as fetch_service
from dataproviders.models import DataProviderUser, DataFileUpload, DataFetch
from dataproviders.models.DataFileSourceBase import DataFileSourceBase
from dataproviders.services import oauth
from dataproviders.services.transform_files_to_data import TransformFilesToData


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


@celery.shared_task
def refresh_access_token(provider_name, user_pk):
    data_provider_user = DataProviderUser.objects.get(user_id=user_pk, data_provider__provider_name=provider_name)
    oauth.refresh_access_token(data_provider_user)


def schedule_task_refresh_access_token(data_provider_user: DataProviderUser):
    if data_provider_user.expires_in and not data_provider_user.has_running_task:
        signature = refresh_access_token.s(data_provider_user.data_provider.provider_name, data_provider_user.pk)
        count_down = calc_countdown(expires_in=data_provider_user.expires_in, buffer=60, min_time=5)
        data_provider_user.apply_async(signature, countdown=count_down)


def calc_countdown(expires_in, buffer, min_time):
    return float(max(expires_in - buffer, min_time))


@celery.shared_task
def clean_data_from_source(data_file_upload_pk, is_from_file_upload: bool):
    data_file_source = get_data_file_source(data_file_upload_pk, is_from_file_upload)
    TransformFilesToData().clean_data_from_data_file_source(data_file_source)


def get_data_file_source(data_file_upload_pk, is_from_file_upload) -> DataFileSourceBase:
    DataObjectClass = DataFileUpload if is_from_file_upload else DataFetch
    data_file_source = DataObjectClass.objects.get(pk=data_file_upload_pk)
    return data_file_source


def schedule_task_clean_data_from_source_file(data_object: DataFileSourceBase):
    if not data_object.has_been_refined:
        is_from_file_upload = isinstance(data_object, DataFileUpload)
        clean_data_from_source.delay(data_object.pk, is_from_file_upload)
