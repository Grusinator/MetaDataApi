from datetime import datetime, timedelta
# from jsonschema import validate
from urllib import request

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.dataproviders.services.url_format_helper import UrlFormatHelper
from MetaDataApi.metadata.models import (
    Schema)
from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider import Endpoint
from MetaDataApi.metadata.services.all_services.base_functions import BaseMetaDataService
from MetaDataApi.metadata.utils.common_utils import StringUtils
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils


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
        endpoint = Endpoint.get_endpoint_as_object(
            self.dataprovider.data_provider_instance,
            endpoint_name
        )

        endpoint.validate()

        endpoint_url = UrlFormatHelper.build_args_for_url(
            endpoint.endpoint_url.value,
            StartDateTime=datetime.now() - timedelta(days=30),
            EndDateTime=datetime.now(),
            AuthToken=auth_token
        )

        url = UrlFormatHelper.join_urls(self.dataprovider.api_endpoint, endpoint_url)

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
