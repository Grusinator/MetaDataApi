import logging
from datetime import datetime, timedelta
from typing import List

import requests
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from MetaDataApi.utils import JsonUtils
from MetaDataApi.utils.django_utils import django_file_utils
from MetaDataApi.utils.django_utils.django_file_utils import FileType
from dataproviders.models import DataProvider, DataFetch, Endpoint, HttpConfig
from dataproviders.models.AuthType import AuthType
from dataproviders.models.UrlArgType import UrlArgType
from dataproviders.services.url_args_formatter.args_rule_types import StartDateTime, EndDateTime, AuthToken, \
    PageCurrent, PageSize
from dataproviders.services.url_args_formatter.base_url_arg_formatting_rule import BaseUrlArgValue
from dataproviders.services.url_args_formatter.url_formatter import UrlFormatter

logger = logging.getLogger(__name__)
MAX_PAGES = 1000
ELEMENTS_PR_PAGE = 1000


def fetch_data_from_endpoint(provider_name, endpoint_name, user_pk, **kwargs):
    data_provider = DataProvider.objects.get(provider_name=provider_name)
    user = User.objects.get(pk=user_pk)
    endpoint = _get_endpoint(data_provider, endpoint_name)
    access_token = try_get_access_token_from_data_provider_user(provider_name, user, endpoint)
    data = fetch_data_from_endpoint_paged(access_token, endpoint)
    data = JsonUtils.clean(data)
    _save_data_to_file(endpoint, user, data)
    return data


def is_endpoint_paged(endpoint):
    return endpoint.url_args.filter(arg_type=UrlArgType.PAGE_CURRENT.get_value()).first()


def fetch_data_from_endpoint_paged(access_token, endpoint):
    if is_endpoint_paged(endpoint):
        # we assume that a page contains lists, and we dont care about data that is not in the list
        data = []
        for page_nr in range(MAX_PAGES):
            url_arg_values = build_url_arg_values(access_token, page_nr)
            data_from_page = _fetch_data_from_endpoint(endpoint, url_arg_values)
            if len(data_from_page) == 0:
                break
            data.extend(data_from_page)
    else:
        url_arg_values = build_url_arg_values(access_token)
        data = _fetch_data_from_endpoint(endpoint, url_arg_values)
    return data


def build_url_arg_values(access_token, page_nr=0):
    return [
        StartDateTime(datetime.now() - timedelta(days=30)),
        EndDateTime(datetime.now()),
        AuthToken(access_token),
        PageCurrent(page_nr, ELEMENTS_PR_PAGE),
        PageSize(ELEMENTS_PR_PAGE)
    ]


def extract_data_structure_at_root(data, endpoint):
    if endpoint.data_structure_root:
        for path in endpoint.data_structure_root.split("."):
            data = data[path]
    return data


def try_get_access_token_from_data_provider_user(provider_name, user, endpoint) -> str:
    if endpoint.requires_auth:
        data_provider_user = user.data_provider_users.get(data_provider__provider_name=provider_name)
        return data_provider_user.access_token


def _fetch_data_from_endpoint(endpoint: Endpoint, url_arg_values: List[BaseUrlArgValue]):
    body, header, url = _build_request(endpoint, url_arg_values)
    data = _request_from_endpoint(url, body, header)
    data = extract_data_structure_at_root(data, endpoint)
    return data


def _build_request(endpoint, url_arg_values):
    url = _build_url(endpoint, url_arg_values)
    body = _build_body(endpoint)
    header = _build_header(endpoint, url_arg_values)
    return body, header, url


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


def _build_header(endpoint: Endpoint, url_arg_values: List[BaseUrlArgValue]):
    header = {}
    try:
        header += endpoint.data_provider.http_config.build_header()
    except HttpConfig.DoesNotExist:
        logger.warning("dataprovider has no http config, so header will be default")
    if endpoint.auth_type == AuthType.OAUTH2.value:
        access_token = next(filter(lambda x: isinstance(x, AuthToken), url_arg_values)).value
        header["Authorization"] = "Bearer %s" % access_token
    return header


def _build_body(endpoint):
    return {}


def _build_url(endpoint, url_arg_values: List[BaseUrlArgValue]):
    endpoint_url = UrlFormatter.build_args_for_url(endpoint, url_arg_values)
    return UrlFormatter.join_urls(endpoint.data_provider.api_endpoint, endpoint_url)
