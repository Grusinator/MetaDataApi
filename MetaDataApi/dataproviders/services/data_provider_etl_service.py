from datetime import datetime, timedelta
# from jsonschema import validate
from urllib import request

from MetaDataApi.dataproviders.services.url_format_helper import UrlFormatHelper
from MetaDataApi.metadata.models import (
    Schema)
from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import gDataProvider
from MetaDataApi.metadata.services.all_services.base_functions import BaseMetaDataService
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils


class DataProviderEtlService:

    def __init__(self, dataprovider: gDataProvider):
        self.dataprovider = dataprovider

    def validate_endpoints(self):
        pass

    def get_related_schema(self):
        schema = BaseMetaDataService.do_meta_item_exists(
            Schema(label=self.dataprovider.data_provider_name)
        )
        return schema or Schema.create_new_empty_schema(
            self.dataprovider.data_provider_name)

    def read_data_from_endpoint(self, endpoint_name: str, auth_token: str = None):
        dp = self.dataprovider
        endpoint = next(filter(lambda x: x.endpoint_name == endpoint_name, dp.endpoints), None)
        endpoint.validate()
        endpoint.data_provider.validate()

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
        endpoint = RdfsDataProvider.get_endpoint(
            self.dataprovider.data_provider_instance,
            rest_endpoint_name=endpoint_name
        )
        file = DjangoModelUtils.convert_str_to_file(data, filetype=DjangoModelUtils.FileType.JSON)
        RdfsDataProvider.create_data_dump(endpoint, file)
