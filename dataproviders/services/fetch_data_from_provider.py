import logging
from datetime import datetime, timedelta

import requests
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from MetaDataApi.utils import JsonUtils
from MetaDataApi.utils.django_utils import django_file_utils
from MetaDataApi.utils.django_utils.django_file_utils import FileType
from dataproviders.models import DataProvider, DataFetch, Endpoint, HttpConfig
from dataproviders.models.AuthType import AuthType
from dataproviders.services.url_args_formatter.url_formatter import UrlFormatter

logger = logging.getLogger(__name__)


def fetch_data_from_endpoint(provider_name, endpoint_name, user_pk):
    data_provider = DataProvider.objects.get(provider_name=provider_name)
    user = User.objects.get(pk=user_pk)
    endpoint = _get_endpoint(data_provider, endpoint_name)
    access_token = try_get_access_token_from_data_provider_user(provider_name, user, endpoint)
    data = _fetch_data_from_endpoint(endpoint, access_token)
    data = JsonUtils.clean(data)
    _save_data_to_file(endpoint, user, data)
    return data


def try_get_access_token_from_data_provider_user(provider_name, user, endpoint) -> str:
    if endpoint.requires_auth:
        data_provider_user = user.data_provider_users.get(data_provider__provider_name=provider_name)
        return data_provider_user.access_token


def _fetch_data_from_endpoint(endpoint: Endpoint, access_token: str = None):
    url = _build_url(endpoint, access_token)
    body = _build_body(endpoint)
    header = _build_header(endpoint, access_token)
    data = _request_from_endpoint(url, body, header)
    return data


def _get_endpoint(data_provider, endpoint_name) -> Endpoint:
    # TODO Endpoint should be identified uniquely by some means but for now this works fine
    try:
        endpoint = data_provider.endpoints.get(endpoint_name=endpoint_name)
    except MultipleObjectsReturned as e:
        logger.warning(e)
        endpoint = data_provider.endpoints.filter(endpoint_name=endpoint_name).first()
    return endpoint


def _request_from_endpoint(url, body, header):
    r = requests.get(url, body, headers=header)
    r.raise_for_status()
    return r.json()


def _save_data_to_file(endpoint: Endpoint, user: User, data: str):
    data_file = django_file_utils.convert_str_to_file(data, filetype=FileType.JSON,
                                                      filename_based_on=endpoint.endpoint_name)
    return DataFetch.objects.create(endpoint=endpoint, data_file_from_source=data_file, user=user,
                                    data_provider=endpoint.data_provider)


def _build_header(endpoint: Endpoint, access_token: str):
    header = {}
    try:
        header += endpoint.data_provider.http_config.build_header()
    except HttpConfig.DoesNotExist:
        logger.warning("dataprovider has no http config, so header will be default")
    if endpoint.auth_type == AuthType.TOKEN.value:
        header["Authorization"] = "Bearer %s" % access_token
    return header


def _build_body(endpoint):
    return {}


def _build_url(endpoint, access_token):
    kwargs = {
        "StartDateTime": datetime.now() - timedelta(days=30),
        "EndDateTime": datetime.now(),
        "AuthToken": access_token
    }
    endpoint_url = UrlFormatter.build_args_for_url(endpoint.endpoint_url, **kwargs)
    return UrlFormatter.join_urls(endpoint.data_provider.api_endpoint, endpoint_url)
