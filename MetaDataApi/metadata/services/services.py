import json
import os
import shutil
from datetime import datetime

from django.contrib.auth.models import User
from graphql import GraphQLError

from MetaDataApi.dataproviders.models import DataDump, DataProvider
from MetaDataApi.metadata.models import *
from MetaDataApi.metadata.utils import JsonUtils
from MetaDataApi.metadata.utils.common_utils import StringUtils
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils
from MetaDataApi.settings import MEDIA_ROOT
from .all_services import *
from ...dataproviders.services import fetch_data_from_provider


def DeleteSchemaService(schema_label):
    if schema_label == "all":
        schemas = Schema.objects.all()
        [schema.delete() for schema in schemas]

        try:
            media_schema_folder = os.path.join(MEDIA_ROOT, "schemas")
            # delete all files in media/schemas folder
            shutil.rmtree(media_schema_folder)
            os.makedirs(media_schema_folder)
        except:
            print("does not work on AWS, and neither needed")
    else:
        schema = Schema.objects.get(label=schema_label)
        schema.delete()


def ExportSchemaService(schema_label):
    service = RdfSchemaService()
    schema = Schema.exists_by_label(schema_label)
    service.export_schema_from_db(schema)
    schema.url = schema.rdfs_file.url
    schema.save()
    return schema.url


def IdentifySchemaFromFileService(self):
    file = next(self.files.values())
    schema_label = self.cleaned_data['schema_label']
    data_label = self.cleaned_data['data_label']
    identify = JsonAnalyser()
    data = json.loads(file.read())
    data_label = data_label or StringUtils.standardize_string(
        file.name, remove_version=True)
    # here we have no idea about the origin if not specified
    # TODO: consider if its better to do something else
    schema = BaseMetaDataService.do_meta_item_exists(
        Schema(label=schema_label))
    if not schema:
        schema = Schema.create_new_empty_schema(schema_label)
    objects = identify.identify_from_json_data(
        data, schema, data_label)
    return objects


def IdentifyDataFromFileService(file, schema_label, data_label, user_pk):
    user = User.objects.get(pk=user_pk)
    identify = JsonAnalyser()
    data = json.loads(file.read())
    data_label = data_label or StringUtils.standardize_string(
        file.name, remove_version=True)
    # here we have no idea about the origin if not specified
    # TODO: consider if its better to do something else
    schema = BaseMetaDataService.do_meta_item_exists(
        Schema(label=schema_label))
    objects = identify.identify_from_json_data(
        data, schema, user, data_label)
    return objects


def IdentifySchemaFromProviderService(provider_name, endpoint, user_pk):
    user = User.objects.get(pk=user_pk)
    identify = JsonAnalyser()
    provider_profile = user.profile.get_data_provider_profile(provider_name)
    schema = Schema.objects.get(label=provider_name)
    data_provider = DataProvider.objects.get(provider_name=provider_name)
    if endpoint == "all" or endpoint is None:
        endpoints = json.loads(data_provider.rest_endpoints_list)
    else:
        endpoints = [endpoint, ]
    n_objs = 0
    for endpoint in endpoints:
        data = fetch_data_from_provider.fetch_data_from_provider_endpoint(endpoint, provider_profile.access_token,
                                                                          user_pk)
        json_data = JsonUtils.validate(data)
        parrent_label = BaseMetaDataService.rest_endpoint_to_label(endpoint)
        objects = identify.identify_from_json_data(json_data, schema, user, parrent_label)
        n_objs += len(objects)

    return n_objs


def IdentifyDataFromProviderService(provider_name, endpoint, user_pk):
    user = User.objects.get(pk=user_pk)
    data_provider = DataProvider.objects.get(provider_name=provider_name)

    identify = JsonAnalyser()

    rdf_service = RdfInstanceService()

    provider_profile = user.profile.get_data_provider_profile(
        provider_name)

    schema = rdf_service.do_meta_item_exists(Schema(label=provider_name))

    # select which endpoints
    if endpoint == "all" or endpoint is None:
        endpoints = json.loads(data_provider.rest_endpoints_list)
    else:
        endpoints = [endpoint, ]

    # identify objects for each endpoint
    schema_nodes = []
    for endpoint in endpoints:
        data = fetch_data_from_provider.fetch_data_from_provider_endpoint(endpoint, provider_profile.access_token,
                                                                          user_pk)
        json_data = JsonUtils.validate(data)

        parrent_label = BaseMetaDataService.rest_endpoint_to_label(
            endpoint)

        objects = identify.identify_from_json_data(
            json_data, schema, parrent_label)
        schema_nodes.extend(objects)

    # generate rdf file from data
    rdf_file = rdf_service.export_instances_to_rdf_file(
        schema, objects)

    return rdf_file, schema_nodes


def LoadSchemaAndDataFromDataDump(data_dump_pk, user_pk):
    user = User.objects.get(pk=user_pk)
    identify = JsonAnalyser()
    data_dump = DataDump(data_dump_pk)
    parrent_label = data_dump.endpoint.name
    data_as_str = DjangoModelUtils.convert_file_to_str(data_dump.file)
    data_as_json = JsonUtils.validate(data_as_str)
    schema = data_dump.endpoint.data_provider.schema
    objects = identify.identify_from_json_data(data_as_json, schema, user, parrent_label)
    service = RdfSchemaService()
    service.export_schema_from_db(schema)
    DataDump(data_dump_pk).loaded = True
    return objects


def AddJsonSchemaService(url, schema_label, user_pk):
    user = User.objects.get(pk=user_pk)
    service = JsonSchemaService()
    if url == "open_m_health":
        try:
            service.write_to_db_baseschema()
            # import threading
            # task = service.write_to_db_baseschema
            # thr = threading.Thread(target=task)
            # thr.start()  # Will run
        except Exception as e:
            raise GraphQLError(str(e))
    elif url == "open_m_health_sample":
        service.write_to_db_baseschema(sample=True)
    else:
        try:
            service.write_to_db(url, schema_label)
        except Exception as e:
            raise GraphQLError(str(e))
    return service.touched_meta_items, service._error_list


def AddRdfSchemaService(url):
    service = RdfSchemaService()
    if url == "baseschema":
        try:
            service.write_to_db_baseschema()
        except Exception as e:
            raise GraphQLError(str(e))
    else:
        try:
            service.write_to_db(url)
        except Exception as e:
            raise GraphQLError(str(e))


def AddPersonReferenceToBaseObjects(schema_label):
    service = DataCleaningService()
    schema = service.do_meta_item_exists(Schema(label=schema_label))
    try:
        objects = service.relate_root_classes_to_foaf(schema)
    except Exception as e:
        raise GraphQLError(str(e))
    return objects


def GetTemporalFloatPairsService(schema_label, object_label, attribute_label, datetime_label, datetime_object_label):
    value_att = SchemaAttribute.objects.get(
        label=attribute_label,
        object__label=object_label,
        object__schema__label=schema_label)
    SchemaAttribute.assert_data_type(value_att, float)
    if datetime_label:
        datetime_att = SchemaAttribute.objects.get(
            label=datetime_label,
            object__label=datetime_object_label or object_label,
            object__schema__label=schema_label
        )
        SchemaAttribute.assert_data_type(datetime_att, datetime)
    else:
        raise NotImplementedError(
            "identify not implemented, specify a secondary label")
        datetime_att = identify()
    service = BaseMetaDataService()
    data = service.get_connected_attribute_pairs(value_att, datetime_att)
    # data_values = [(att_inst1.value, att_inst2.value)
    #                for att_inst1, att_inst2 in data]
    return data
