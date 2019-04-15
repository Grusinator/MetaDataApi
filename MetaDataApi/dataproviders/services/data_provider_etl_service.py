import json
from datetime import datetime, timedelta
# from jsonschema import validate
from urllib import request

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.dataproviders.services.url_format_helper import UrlFormatHelper
from MetaDataApi.metadata.models import (
    Schema)
from MetaDataApi.metadata.rdf_models import RdfDataProvider
from MetaDataApi.metadata.services.all_services.base_functions import BaseMetaDataService
from MetaDataApi.metadata.utils.common_utils import StringUtils


class DataProviderEtlService:

    def __init__(self, dataprovider: DataProvider):
        self.dataprovider = dataprovider if \
            isinstance(dataprovider, DataProvider) else \
            DataProvider.objects.get(
                provider_name=StringUtils.standardize_string(dataprovider))

    def validate_endpoints(self):
        pass

    def get_related_schema(self):
        schema = BaseMetaDataService.do_meta_item_exists(
            Schema(label=self.dataprovider.provider_name)
        )
        return schema or Schema.create_new_empty_schema(
            self.dataprovider.provider_name)

    def read_data_from_endpoint(self, endpoint_name: str, auth_token: str = None):
        endpoint = RdfDataProvider.get_endpoint_as_object(
            self.dataprovider.data_provider_instance,
            endpoint_name
        )

        endpoint_url = UrlFormatHelper.build_args_for_url(
            endpoint.url,
            StartDateTime=datetime.now() - timedelta(days=30),
            EndDateTime=datetime.now(),
            AuthToken=auth_token)

        url = UrlFormatHelper.join_urls(self.dataprovider.api_endpoint, endpoint_url)

        data = self.request_json_from_endpoint(auth_token, url)
        return data

    @staticmethod
    def request_json_from_endpoint(auth_token, url):
        header = {"Authorization": "Bearer %s" % auth_token}
        req = request.Request(url, None, header)
        response = request.urlopen(req)
        html = response.read()
        json_obj = json.loads(html)
        return json_obj

    def save_data_to_file(self, endpoint_name: str, data: str):
        endpoint = RdfDataProvider.get_endpoint(
            self.dataprovider.data_provider_instance,
            rest_endpoint_name=endpoint_name
        )
        file = RdfDataProvider.create_file_from_str(data)
        RdfDataProvider.create_data_dump(endpoint, file)
