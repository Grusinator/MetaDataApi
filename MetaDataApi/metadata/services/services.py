import json
from django import forms

from service_objects.services import Service

from MetaDataApi.metadata.services import *

from MetaDataApi.metadata.models import *
from django.contrib.auth.models import User

from MetaDataApi.dataproviders.models import ThirdPartyDataProvider

from MetaDataApi.dataproviders.services.data_provider_etl_service import DataProviderEtlService


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

        schema = service._try_get_item(Schema(label=schema_label))

        service.export_schema_from_db(schema)

        schema_file_url = schema.rdfs_file.url
        return schema_file_url


class IdentifySchemaFromFileService(Service):
    file = forms.FileField()
    schema_label = forms.CharField()

    def process(self):
        file = self.cleaned_data['file']
        schema_label = self.cleaned_data['schema_label']

        identify = SchemaIdentificationV2()

        with open(uploaded_file) as f:
            data = json.loads(f)

        # here we have no idea about the origin if not specified
        # TODO: consider if its better to do something else
        schema = identify._try_create_item(Schema(label=schema_label))

        objects = identify.identify_schema_from_dataV2(
            data, schema)

        return objects


class IdentifyDataFromFileService(Service):
    schema_label = forms.CharField()
    file = forms.FileField()
    data_label = forms.CharField()
    user_pk = forms.IntegerField()

    def process(self):
        file = self.cleaned_data['file']
        schema_label = self.cleaned_data['schema_label']
        data_label = self.cleaned_data['data_label']
        user_pk = self.cleaned_data['user_pk']
        user = User.objects.get(pk=user_pk)

        identify = SchemaIdentificationV2()

        uploaded_file = info.context.FILES.get(file)
        with open(uploaded_file) as f:
            data = json.loads(f)

        # here we have no idea about the origin if not specified
        # TODO: consider if its better to do something else
        schema = identify._try_get_item(Schema(label=schema_label))

        objects = identify.map_data_to_native_instances(
            data, schema, data_label)

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

        identify = SchemaIdentificationV2()
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

            parrent_label = identify.rest_endpoint_to_label(endpoint)

            objects = identify.identify_schema_from_dataV2(
                data, schema, parrent_label)
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

        identify = SchemaIdentificationV2()
        provider_service = DataProviderEtlService(provider_name)
        rdf_service = RdfInstanceService()

        provider_profile = user.profile.get_data_provider_profile(
            provider_name)

        schema = rdf_service._try_get_item(Schema(label=provider_name))

        # select which endpoints
        if endpoint == "all" or endpoint is None:
            endpoints = json.loads(
                provider_service.dataprovider.rest_endpoints_list)
        else:
            endpoints = [endpoint, ]

        # identify objects for each endpoint
        object_list = []
        for endpoint in endpoints:
            data = provider_service.read_data_from_endpoint(
                endpoint, provider_profile.access_token)

            parrent_label = identify.rest_endpoint_to_label(endpoint)

            objects = identify.map_data_to_native_instances(
                data, schema, parrent_label)
            object_list.extend(objects)

        # generate rdf file from data
        rdf_file = rdf_service.export_instances_to_rdf_file(
            schema, objects)

        return rdf_file, object_list


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
                raise GraphQLError(e)
        elif url == "open_m_health_sample":
            service.write_to_db_baseschema(sample=True)
        else:
            try:
                service.write_to_db(url, name)
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

        schema = service._try_get_item(Schema(label=schema_label))

        try:
            objects = service.relate_root_classes_to_foaf(schema)
        except Exception as e:
            raise GraphQLError(str(e))

        return objects
