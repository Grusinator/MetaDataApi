import os
import shutil
import graphene
import json
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User
from MetaDataApi.settings import MEDIA_ROOT


from MetaDataApi.users.schema import UserType
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation, UnmappedObject)
from MetaDataApi.metadata.services import (
    RdfSchemaService,
    RdfInstanceService,
    JsonSchemaService,
    SchemaIdentificationV2,
    DataCleaningService)

from MetaDataApi.dataproviders.models import ThirdPartyDataProvider

from MetaDataApi.dataproviders.services.data_provider_etl_service import (
    DataProviderEtlService)


class SchemaNode(DjangoObjectType):
    class Meta:
        model = Schema
        filter_fields = ['label', 'description']
        interfaces = (graphene.relay.Node, )


class ObjectNode(DjangoObjectType):
    class Meta:
        model = Object
        filter_fields = ['label', 'description']
        interfaces = (graphene.relay.Node, )


class AttributeNode(DjangoObjectType):
    class Meta:
        model = Attribute
        filter_fields = ['label', ]
        interfaces = (graphene.relay.Node, )


class ObjectRelationNode(DjangoObjectType):
    class Meta:
        model = ObjectRelation
        filter_fields = ['label', ]
        interfaces = (graphene.relay.Node, )


class DeleteSchema(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        schema_name = graphene.String()

    @login_required
    def mutate(self, info, schema_name):
        if schema_name == "all":
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
            schema = Schema.objects.get(label=schema_name)
            schema.delete()

        return DeleteSchema(success=True)


class ExportSchema(graphene.Mutation):
    schema_file_url = graphene.String()
    visualization_url = graphene.String()
    data = graphene.String()

    class Arguments:
        schema_name = graphene.String()

    def mutate(self, info, schema_name):
        service = RdfSchemaService()

        schema = service.export_schema_from_db(schema_name)

        schema_file_url = schema.rdfs_file.url

        g = service._create_graph_from_url(schema_file_url)

        data = g.serialize(format='turtle')

        return ExportSchema(
            schema_file_url=schema_file_url,
            visualization_url="http://visualdataweb.de/webvowl/#iri=" +
            schema_file_url,
            data=data)


class IdentifyData(graphene.Mutation):
    modified_data = graphene.String()
    identified_objects = graphene.Int()

    class Arguments:
        input_data = graphene.String()

    @login_required
    def mutate(self, info, input_data):
        identify = SchemaIdentificationV2()

        # here we have no idea about the origin if not specified
        # TODO: consider if its better to do something else

        modified_data, objects = identify.create_instances_from_data(
            input_data)

        return IdentifyData(modified_data=modified_data,
                            identified_objects=len(objects))


class IdentifyDataFromProvider(graphene.Mutation):
    modified_data = graphene.String()
    identified_objects = graphene.Int()
    rdf_dump_url = graphene.String()

    class Arguments:
        provider_name = graphene.String()
        endpoint = graphene.String()

    @login_required
    def mutate(self, info, provider_name, endpoint):
        identify = SchemaIdentificationV2()
        provider_service = DataProviderEtlService(provider_name)
        rdf_service = RdfInstanceService()

        profile = info.context.user.profile

        provider_profile = profile.get_data_provider_profile(provider_name)

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

            modified_data, objects = identify.map_data_to_native_instances(
                data, provider_name, parrent_label)
            object_list.extend(objects)

        # generate rdf file from data
        rdf_file = rdf_service.export_instances_to_rdf_file(
            provider_name, objects)

        return IdentifyDataFromProvider(modified_data=modified_data,
                                        identified_objects=len(object_list),
                                        rdf_dump_url=rdf_file.url)


class IdentifySchemaFromProvider(graphene.Mutation):
    identified_objects = graphene.Int()

    class Arguments:
        provider_name = graphene.String()
        endpoint = graphene.String()

    @login_required
    def mutate(self, info, provider_name, endpoint=None):
        identify = SchemaIdentificationV2()
        provider_service = DataProviderEtlService(provider_name)

        profile = info.context.user.profile
        provider_profile = profile.get_data_provider_profile(provider_name)

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
                data, provider_name, parrent_label)
            n_objs += len(objects)

        return IdentifyDataFromProvider(identified_objects=n_objs)


class AddJsonSchema(graphene.Mutation):
    succes = graphene.Boolean()
    objects_added = graphene.Int()
    objects_failed = graphene.Int()

    class Arguments:
        url = graphene.String()
        name = graphene.String()

    @login_required
    def mutate(self, info, url, name):
        service = JsonSchemaService()
        if url == "open_m_health":
            try:

                import threading
                task = service.write_to_db_baseschema
                thr = threading.Thread(target=task)
                thr.start()  # Will run

            except Exception as e:
                raise GraphQLError(e)
        elif url == "open_m_health_sample":
            service.write_to_db_baseschema(sample=True)
        else:
            try:
                service.write_to_db(url, name)
            except Exception as e:
                raise GraphQLError(str(e))

        return AddJsonSchema(
            succes=True,
            objects_added=len(service.touched_meta_items),
            objects_failed=len(service._error_list))


class AddRdfSchema(graphene.Mutation):
    succes = graphene.Boolean()
    objects_added = graphene.Int()

    class Arguments:
        url = graphene.String()

    @login_required
    def mutate(self, info, url):
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

        return AddRdfSchema(succes=True)


class AddPersonReference(graphene.Mutation):
    succes = graphene.Boolean()
    objects_added = graphene.Int()

    class Arguments:
        url = graphene.String()

    @login_required
    def mutate(self, info, url):
        service = DataCleaningService()
        try:
            objects = service.relate_root_classes_to_foaf(url)
        except Exception as e:
            raise GraphQLError(str(e))

        return AddPersonReference(succes=True, objects_added=len(objects))


# wrap all queries and mutations


class Query(graphene.ObjectType):
    schema = graphene.relay.Node.Field(SchemaNode)
    all_schemas = DjangoFilterConnectionField(SchemaNode)

    object = graphene.relay.Node.Field(ObjectNode)
    all_objects = DjangoFilterConnectionField(ObjectNode)

    attribute = graphene.relay.Node.Field(AttributeNode)
    all_attributes = DjangoFilterConnectionField(AttributeNode)

    object_relation = graphene.relay.Node.Field(ObjectRelationNode)
    all_object_relations = DjangoFilterConnectionField(ObjectRelationNode)

    # def resolve_schema(self, info):
    #     return Schema.objects.first()

    # def resolve_all_schema(self, info):
    #     return Schema.objects.all()

    # # objects
    # def resolve_object(self, info):
    #     return Object.objects.first()

    # def resolve_all_objects(self, info):
    #     return Object.objects.all()

    # # attributes
    # def resolve_attribute(self, info):
    #     return Attribute.objects.first()

    # def resolve_all_attributes(self, info):
    #     return Attribute.objects.all()

    # # object relations
    # def resolve_object_relation(self, info):
    #     return ObjectRelation.objects.first()

    # def resolve_all_object_relations(self, info):
    #     return ObjectRelation.objects.all()


class Mutation(graphene.ObjectType):
    add_rdf_schema = AddRdfSchema.Field()
    add_json_schema = AddJsonSchema.Field()
    delete_schema = DeleteSchema.Field()
    identify_data = IdentifyData.Field()
    export_schema = ExportSchema.Field()
    add_person_reference = AddPersonReference.Field()
    identify_data_from_provider = IdentifyDataFromProvider.Field()
    identify_schema_from_provider = IdentifySchemaFromProvider.Field()
