import json
import os
import shutil
from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from graphql import GraphQLError
from service_objects.services import Service

from MetaDataApi.dataproviders.models import DataDump
from MetaDataApi.dataproviders.services.data_provider_etl_service import DataProviderEtlService
from MetaDataApi.metadata.models import *
from MetaDataApi.metadata.utils import JsonUtils
from MetaDataApi.metadata.utils.common_utils import StringUtils
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils
from MetaDataApi.settings import MEDIA_ROOT
from .all_services import *


class DeleteSchemaService(Service):
    schema_label = forms.CharField()

    def process(self):
        schema_label = self.cleaned_data['schema_label']

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


class ExportSchemaService(Service):
    schema_label = forms.CharField()

    def process(self):
        schema_label = self.cleaned_data['schema_label']

        service = RdfSchemaService()
        schema = Schema.exists_by_label(schema_label)
        service.export_schema_from_db(schema)
        schema.url = schema.rdfs_file.url
        schema.save()
        return schema.url


class IdentifySchemaFromFileService(Service):
    file = forms.FileField(required=False)
    schema_label = forms.CharField()
    data_label = forms.CharField(required=False)

    def process(self):
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


class IdentifyDataFromFileService(Service):
    schema_label = forms.CharField()
    file = forms.FileField(required=False)
    data_label = forms.CharField(required=False)
    user_pk = forms.IntegerField()

    def process(self):
        file = next(self.files.values())
        schema_label = self.cleaned_data['schema_label']
        data_label = self.cleaned_data['data_label']
        user_pk = self.cleaned_data['user_pk']
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


class IdentifySchemaFromProviderService(Service):
    provider_name = forms.CharField()
    endpoint = forms.CharField()
    user_pk = forms.IntegerField()

    def process(self):
        provider_name = self.cleaned_data['provider_name']
        endpoint = self.cleaned_data['endpoint']
        user_pk = self.cleaned_data['user_pk']
        user = User.objects.get(pk=user_pk)

        identify = JsonAnalyser()
        provider_service = DataProviderEtlService(provider_name)

        provider_profile = user.profile.get_data_provider_profile(
            provider_name)

        schema = provider_service.get_related_schema()

        if endpoint == "all" or endpoint is None:
            endpoints = json.loads(
                provider_service.dataprovider.rest_endpoints_list)
        else:
            endpoints = [endpoint, ]
        n_objs = 0
        for endpoint in endpoints:
            data = provider_service.read_data_from_endpoint(
                endpoint, provider_profile.access_token)

            json_data = JsonUtils.validate(data)

            parrent_label = BaseMetaDataService.rest_endpoint_to_label(
                endpoint)

            objects = identify.identify_from_json_data(
                json_data, schema, user, parrent_label)
            n_objs += len(objects)

        return n_objs


class IdentifyDataFromProviderService(Service):
    provider_name = forms.CharField()
    endpoint = forms.CharField()
    user_pk = forms.IntegerField()

    def process(self):
        provider_name = self.cleaned_data['provider_name']
        endpoint = self.cleaned_data['endpoint']
        user_pk = self.cleaned_data['user_pk']
        user = User.objects.get(pk=user_pk)

        identify = JsonAnalyser()
        provider_service = DataProviderEtlService(provider_name)
        rdf_service = RdfInstanceService()

        provider_profile = user.profile.get_data_provider_profile(
            provider_name)

        schema = rdf_service.do_meta_item_exists(Schema(label=provider_name))

        # select which endpoints
        if endpoint == "all" or endpoint is None:
            endpoints = json.loads(
                provider_service.dataprovider.rest_endpoints_list)
        else:
            endpoints = [endpoint, ]

        # identify objects for each endpoint
        schema_nodes = []
        for endpoint in endpoints:
            data = provider_service.read_data_from_endpoint(
                endpoint, provider_profile.access_token)

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


class LoadSchemaAndDataFromDataDump(Service):
    data_dump_pk = forms.CharField()
    user_pk = forms.IntegerField()

    def process(self):
        data_dump_pk = self.cleaned_data['data_dump_pk']
        user_pk = self.cleaned_data['user_pk']
        user = User.objects.get(pk=user_pk)

        identify = JsonAnalyser()

        data_dump = DataDump(data_dump_pk)
        parrent_label = data_dump.endpoint.name

        data_as_str = DjangoModelUtils.convert_file_to_str(data_dump.file)
        data_as_json = JsonUtils.validate(data_as_str)

        schema = data_dump.endpoint.data_provider.schema

        objects = identify.identify_from_json_data(
            data_as_json, schema, user, parrent_label)

        service = RdfSchemaService()
        service.export_schema_from_db(schema)

        DataDump(data_dump_pk).loaded = True

        return objects


class AddJsonSchemaService(Service):
    url = forms.CharField()
    schema_label = forms.CharField()
    user_pk = forms.IntegerField()

    def process(self):
        url = self.cleaned_data['url']
        schema_label = self.cleaned_data['schema_label']
        user_pk = self.cleaned_data['user_pk']
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


class AddRdfSchemaService(Service):
    url = forms.CharField()

    def process(self):
        url = self.cleaned_data['url']

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


class AddPersonReferenceToBaseObjects(Service):
    schema_label = forms.CharField()

    def process(self):
        schema_label = self.cleaned_data['schema_label']

        service = DataCleaningService()

        schema = service.do_meta_item_exists(Schema(label=schema_label))

        try:
            objects = service.relate_root_classes_to_foaf(schema)
        except Exception as e:
            raise GraphQLError(str(e))

        return objects


class GetTemporalFloatPairsService(Service):
    schema_label = forms.CharField()
    object_label = forms.CharField()
    attribute_label = forms.CharField()
    datetime_label = forms.CharField(required=False)
    datetime_object_label = forms.CharField(required=False)

    def process(self):
        schema_label = self.cleaned_data['schema_label']
        object_label = self.cleaned_data['object_label']
        attribute_label = self.cleaned_data['attribute_label']
        datetime_label = self.cleaned_data['datetime_label']
        datetime_object_label = self.cleaned_data['datetime_object_label']

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
