import json
import os
import re
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


import inflection

# from jsonschema import validate
from urllib import request, parse
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

from MetaDataApi.dataproviders.default_3rd_data_providers import (
    default_data_providers)
from MetaDataApi.dataproviders.models import (
    ThirdPartyDataProvider)


class DataProviderEtlService():  # BaseMetaDataService):

    def __init__(self, dataprovider):
        # super(JsonSchemaService, self).__init__()

        self.dataprovider = dataprovider if \
            isinstance(dataprovider, ThirdPartyDataProvider) else \
            ThirdPartyDataProvider.objects.get(provider_name=dataprovider)

    def validate_endpoints(self):
        self.dataprovider

    def get_related_schema(self):
        schema = self._try_get_item(
            Schema(label=self.dataprovider.provider_name)
        )
        return schema or self.create_new_empty_schema(
            self.dataprovider.provider_name)

    def read_data_from_all_rest_endpoints(self, auth_token=None):
        endpoints = json.loads(self.dataprovider.rest_endpoints_list)

        data = [self.read_data_from_endpoint(
            ep, auth_token) for ep in endpoints]

        return data

    def build_args_for_url(self, endpoint, **kwargs):

        self.valid_kwarg_names = [
            "StartDateTime",
            "EndDateTime"
        ]

        for key, value in kwargs.items():
            test = key in self.valid_kwarg_names
            assert key in self.valid_kwarg_names, "invalid args"

        self._data_type_converter = {
            "UTCSEC": lambda x: str(int(x.timestamp()))
        }

        output_endpoint = endpoint

        args = re.findall("{(.*?)}", endpoint)
        for arg in args:
            arg_type, dataformat = arg.split(":")
            assert arg_type in self.valid_kwarg_names, " invald args in endpoint url"
            try:
                value = kwargs[arg_type]
                converter = self._data_type_converter[dataformat]
                string = converter(value)
                output_endpoint = output_endpoint.replace("{%s}" % arg, string)
            except Exception as e:
                a = 1

        return output_endpoint

    def read_data_from_endpoint(self, endpoint, auth_token=None):
        # remove first slash if exists
        endpoint = endpoint[1:] if endpoint[0] == "/" else endpoint

        if endpoint not in self.dataprovider.rest_endpoints_list:
            print("warning: This is not a known %s endpoint - \"%s\" " %
                  (self.dataprovider.provider_name, endpoint))

        dp_base_url = self.dataprovider.api_endpoint
        dp_base_url += "/" if dp_base_url[-1] != "/" else ""

        url = parse.urljoin(dp_base_url, endpoint)
        header = {"Authorization": "Bearer %s" % auth_token}

        req = request.Request(url, None, header)
        response = request.urlopen(req)
        html = response.read()
        json_obj = json.loads(html)
        return json_obj
