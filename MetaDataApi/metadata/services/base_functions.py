import os
import re
from django.db import transaction
import inflection
# from jsonschema import validate
from urllib import request
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

from schemas.json.omh.schema_names import schema_names


def standarize_string(string, remove_version=False):
    string = inflection.underscore(str(string))

    string = string.replace(" ", "_")
    # remove any version numbers
    if remove_version:
        string = re.sub("(|_version|_v|_v.)(|_)\d+\.(\d+|x)(|_)", '', string)

    string = re.sub("(|_)vocabulary(|_)", '', string)

    # remove trailing and leading whitespace/underscore
    # string = re.sub('/^[\W_]+|[\W_]+$/', '', string)

    return string
