from datetime import datetime, timedelta
# from jsonschema import validate
from urllib import request

from MetaDataApi.dataproviders.models import DataProvider, DataDump
from MetaDataApi.dataproviders.services.url_format_helper import UrlFormatHelper
from MetaDataApi.metadata.models import (
    Schema)
from MetaDataApi.metadata.services.all_services.base_functions import BaseMetaDataService
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils


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

    def read_data_from_endpoint(self, endpoint_name: str, auth_token: str = None):
        data_provider = self.data_provider
        endpoint = data_provider.endpoints.get(endpoint_name=endpoint_name)

        endpoint_url = UrlFormatHelper.build_args_for_url(
            endpoint.endpoint_url,
            StartDateTime=datetime.now() - timedelta(days=30),
            EndDateTime=datetime.now(),
            AuthToken=auth_token
        )

        url = UrlFormatHelper.join_urls(endpoint.data_provider.api_endpoint, endpoint_url)

        data = self.request_from_endpoint(auth_token, url)
        return data

    @staticmethod
    def request_from_endpoint(auth_token, url):
        header = {"Authorization": "Bearer %s" % auth_token}
        req = request.Request(url, None, header)
        response = request.urlopen(req)
        html = response.read()

        return html

    def save_data_to_file(self, endpoint_name: str, data: str):
        endpoint = self.data_provider.endpoints.get(endpoint_name=endpoint_name)
        file = DjangoModelUtils.convert_str_to_file(data, filetype=DjangoModelUtils.FileType.JSON)
        DataDump.objects.create(endpoint=endpoint, file=file)
