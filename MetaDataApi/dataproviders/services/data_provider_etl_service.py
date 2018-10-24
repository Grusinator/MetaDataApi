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


class DataProviderEtlService():  # BaseMetaDataService):

    def __init__(self, dataprovider):
        # super(JsonSchemaService, self).__init__()
        self.dataprovider = dataprovider

    def validate_endpoints(self):
        self.dataprovider

    def read_data_from_all_rest_endpoints(self, auth_token=None):
        endpoints = json.loads(self.dataprovider.rest_endpoints_list)

        data = [self.read_data_from_endpoint(
            ep, auth_token) for ep in endpoints]

        return data

    def read_data_from_endpoint(self, endpoint, auth_token=None):
        # remove first slash if exists
        endpoint = endpoint[1:] if endpoint[0] == "/" else endpoint

        url = parse.urljoin(self.dataprovider.api_endpoint, endpoint)
        header = {"Authorization": "Bearer %s" % auth_token}

        req = request.Request(url, None, header)
        response = request.urlopen(req)
        html = response.read()
        json_obj = json.loads(html)
        return json_obj
