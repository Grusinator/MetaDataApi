import logging
from datetime import datetime, timedelta
from urllib import request

from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from MetaDataApi.dataproviders.models import DataProvider, DataDump, Endpoint, HttpConfig
from MetaDataApi.dataproviders.models.ApiTypes import ApiTypes
from MetaDataApi.dataproviders.services.url_format_helper import UrlFormatHelper
from MetaDataApi.metadata.utils import JsonUtils
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils

logger = logging.getLogger(__name__)


def fetch_data_from_endpoint(provider_name, endpoint_name, user_pk):
    data_provider = DataProvider.objects.get(provider_name=provider_name)
    user = User.objects.get(pk=user_pk)
    endpoint = _get_endpoint(data_provider, endpoint_name)
    # get the profile, with the access token matching the provider_name
    third_party_profiles = user.profile.data_provider_profiles
    third_party_profile = third_party_profiles.get(data_provider__provider_name=provider_name)
    data = _fetch_data_from_endpoint(endpoint, third_party_profile.access_token)
    data = JsonUtils.clean(data)
    _save_data_to_file(endpoint, data)


def _fetch_data_from_endpoint(endpoint, access_token: str = None):
    url = _build_url(endpoint, access_token)
    body = _build_body(endpoint)
    header = _build_header(endpoint, access_token)

    data = _request_from_endpoint(url, body, header)
    return data


def _get_endpoint(data_provider, endpoint_name):
    # TODO Endpoint should be identified uniquely by some means but for now this works fine
    try:
        endpoint = data_provider.endpoints.get(endpoint_name=endpoint_name)
    except MultipleObjectsReturned as e:
        logger.warning(e)
        endpoint = data_provider.endpoints.filter(endpoint_name=endpoint_name).first()
    return endpoint


def _request_from_endpoint(url, body, header):
    req = request.Request(url, body, header)
    response = request.urlopen(req)
    html = response.read()
    return html


def _save_data_to_file(endpoint: Endpoint, data: str):
    file = DjangoModelUtils.convert_str_to_file(data, filetype=DjangoModelUtils.FileType.JSON)
    DataDump.objects.create(endpoint=endpoint, file=file)


def _build_header(endpoint: Endpoint, access_token: str):
    header = {}
    try:
        header += endpoint.data_provider.http_config.build_header()
    except HttpConfig.DoesNotExist:
        logger.warning("dataprovider has no http config, so header will be default")

    if endpoint.data_provider.api_type == ApiTypes.OAUTH_REST.value:
        header["Authorization"] = "Bearer %s" % access_token

    return header


def _build_body(endpoint):
    return None


def _build_url(endpoint, access_token):
    endpoint_url = UrlFormatHelper.build_args_for_url(
        endpoint.endpoint_url,
        StartDateTime=datetime.now() - timedelta(days=30),
        EndDateTime=datetime.now(),
        AuthToken=access_token
    )

    return UrlFormatHelper.join_urls(endpoint.data_provider.api_endpoint, endpoint_url)
