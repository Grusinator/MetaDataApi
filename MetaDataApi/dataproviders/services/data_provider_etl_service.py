import logging
from datetime import datetime, timedelta
# from jsonschema import validate
from urllib import request

from django.core.exceptions import MultipleObjectsReturned

from MetaDataApi.dataproviders.models import DataProvider, DataDump, Endpoint
from MetaDataApi.dataproviders.models.ApiTypes import ApiTypes
from MetaDataApi.dataproviders.services.url_format_helper import UrlFormatHelper
from MetaDataApi.metadata.models import (
    Schema)
from MetaDataApi.metadata.services.all_services.base_functions import BaseMetaDataService
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils

logger = logging.getLogger(__name__)

class DataProviderEtlService:

    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider

    def validate_endpoints(self):
        pass

    def get_related_schema(self):
        schema = BaseMetaDataService.do_meta_item_exists(
            Schema(label=self.data_provider.data_provider_name)
        )
        return schema or Schema.create_new_empty_schema(
            self.data_provider.data_provider_name)

    def read_data_from_endpoint(self, endpoint_name: str, access_token: str = None):
        try:
            endpoint = self.data_provider.endpoints.get(endpoint_name=endpoint_name)
        except MultipleObjectsReturned as e:
            logger.warning(e)
            endpoint = self.data_provider.endpoints.filter(endpoint_name=endpoint_name).first()

        url = self.build_url(endpoint, access_token)
        body = self.build_body(endpoint)
        header = self.build_header(endpoint, access_token)

        data = self.request_from_endpoint(url, body, header)
        return data

    @staticmethod
    def request_from_endpoint(url, body, header):
        req = request.Request(url, body, header)
        response = request.urlopen(req)
        html = response.read()
        return html

    def save_data_to_file(self, endpoint_name: str, data: str):
        endpoint = self.data_provider.endpoints.get(endpoint_name=endpoint_name)
        file = DjangoModelUtils.convert_str_to_file(data, filetype=DjangoModelUtils.FileType.JSON)
        DataDump.objects.create(endpoint=endpoint, file=file)

    def build_header(self, endpoint: Endpoint, access_token: str):
        header = endpoint.data_provider.http_config.build_header()
        if endpoint.data_provider.api_type == ApiTypes.OAUTH_REST:
            header["Authorization"] = "Bearer %s" % access_token
        return header

    def build_body(self, endpoint):
        return None

    def build_url(self, endpoint, access_token):
        endpoint_url = UrlFormatHelper.build_args_for_url(
            endpoint.endpoint_url,
            StartDateTime=datetime.now() - timedelta(days=30),
            EndDateTime=datetime.now(),
            AuthToken=access_token
        )

        return UrlFormatHelper.join_urls(endpoint.data_provider.api_endpoint, endpoint_url)
