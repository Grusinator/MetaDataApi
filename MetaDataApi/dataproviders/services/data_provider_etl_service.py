import json
import os
import re
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


import inflection

# from jsonschema import validate
from urllib import request
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
