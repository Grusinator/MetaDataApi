import json
from datetime import datetime, timedelta
# from jsonschema import validate
from urllib import request, parse

from dataproviders.models import ThirdPartyDataProvider
from dataproviders.services.url_argument_format_helper import UrlArgumentFormatHelper
from metadata.models import (
    Schema)
from metadata.services.all_services.base_functions import BaseMetaDataService
from metadata.utils.common_utils import StringUtils


class DataProviderEtlService(BaseMetaDataService):

    def __init__(self, dataprovider):
        super(DataProviderEtlService, self).__init__()

        self.dataprovider = dataprovider if \
            isinstance(dataprovider, ThirdPartyDataProvider) else \
            ThirdPartyDataProvider.objects.get(
                provider_name=StringUtils.standardize_string(dataprovider))

    def validate_endpoints(self):
        pass

    def get_related_schema(self):
        schema = BaseMetaDataService.do_meta_item_exists(
            Schema(label=self.dataprovider.provider_name)
        )
        return schema or BaseMetaDataService.create_new_empty_schema(
            self.dataprovider.provider_name)

    # def read_data_from_all_rest_endpoints(self, auth_token=None):
    #     endpoints = json.loads(self.dataprovider.rest_endpoints_list)

    #     data = [self.read_data_from_endpoint(
    #         ep, auth_token) for ep in endpoints]

    #     return data

    def read_data_from_endpoint(self, endpoint, auth_token=None):
        # remove first slash if exists
        endpoint = endpoint[1:] if endpoint[0] == "/" else endpoint

        if endpoint not in self.dataprovider.rest_endpoints_list:
            print("warning: This is not a known %s endpoint - \"%s\" " %
                  (self.dataprovider.provider_name, endpoint))

        dp_base_url = self.dataprovider.api_endpoint
        dp_base_url += "/" if dp_base_url[-1] != "/" else ""

        endpoint = UrlArgumentFormatHelper.build_args_for_url(
            endpoint,
            StartDateTime=datetime.now() - timedelta(days=30),
            EndDateTime=datetime.now(),
            AuthToken=auth_token)

        url = parse.urljoin(dp_base_url, endpoint)
        header = {"Authorization": "Bearer %s" % auth_token}

        req = request.Request(url, None, header)
        response = request.urlopen(req)
        html = response.read()
        json_obj = json.loads(html)
        return json_obj
