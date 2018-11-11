import os
import shutil
import graphene
import json
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload

from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.models import User
from MetaDataApi.settings import MEDIA_ROOT


from MetaDataApi.users.schema import UserType
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation, UnmappedObject)


from MetaDataApi.dataproviders.models import ThirdPartyDataProvider

from MetaDataApi.dataproviders.services.data_provider_etl_service import (
    DataProviderEtlService)

from MetaDataApi.metadata.services.services import *

from MetaDataApi.metadata.services import *


# Nodes
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


# Mutations
class DeleteSchema(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        schema_label = graphene.String()

    @user_passes_test(lambda u: u.is_superuser)
    def mutate(self, info, schema_label):
        args = dict(locals())
        [args.pop(x) for x in ["info", "self"]]

        DeleteSchemaService.execute(args)

        return DeleteSchema(success=True)


class ExportSchema(graphene.Mutation):
    schema_file_url = graphene.String()
    visualization_url = graphene.String()

    class Arguments:
        schema_label = graphene.String()

    def mutate(self, info, schema_label):
        args = locals()
        [args.pop(x) for x in ["info", "self", "args"]]
        args["user_pk"] = info.context.user.pk

        schema_file_url = ExportSchemaService.execute(args)

        return ExportSchema(
            schema_file_url=schema_file_url,
            visualization_url="http://visualdataweb.de/webvowl/#iri=" +
            schema_file_url)


class IdentifySchemaFromFile(graphene.Mutation):
    identified_objects = graphene.Int()
    success = graphene.Boolean()

    class Arguments:
        file = Upload(required=True)
        schema_label = graphene.String()
        data_label = graphene.String()

    @login_required
    def mutate(self, info, file, schema_label, data_label=None):
        args = locals()
        [args.pop(x) for x in ["info", "self", "args"]]
        args["user_pk"] = info.context.user.pk

        objects = IdentifySchemaFromFileService.execute(
            args, info.context.FILES)

        return IdentifySchemaFromFile(identified_objects=len(objects))


class IdentifyDataFromFile(graphene.Mutation):
    identified_objects = graphene.Int()

    class Arguments:
        file = Upload(required=True)
        schema_label = graphene.String()
        data_label = graphene.String()

    @login_required
    def mutate(self, info, file, schema_label, data_label):
        args = locals()
        [args.pop(x) for x in ["info", "self", "args"]]
        args["user_pk"] = info.context.user.pk

        objects = IdentifyDataFromFileService.execute(args, info.context.FILES)

        return IdentifyDataFromFile(identified_objects=len(objects))


class IdentifySchemaFromProvider(graphene.Mutation):
    identified_objects = graphene.Int()

    class Arguments:
        provider_name = graphene.String()
        endpoint = graphene.String()

    @login_required
    def mutate(self, info, provider_name, endpoint=None):
        args = locals()
        [args.pop(x) for x in ["info", "self", "args"]]
        args["user_pk"] = info.context.user.pk

        n_objs = IdentifySchemaFromProviderService.execute(args)

        return IdentifyDataFromProvider(identified_objects=n_objs)


class IdentifyDataFromProvider(graphene.Mutation):
    identified_objects = graphene.Int()
    rdf_dump_url = graphene.String()

    class Arguments:
        provider_name = graphene.String()
        endpoint = graphene.String()

    @login_required
    def mutate(self, info, provider_name, endpoint):
        args = locals()
        [args.pop(x) for x in ["info", "self", "args"]]
        args["user_pk"] = info.context.user.pk

        rdf_file, object_list = IdentifyDataFromProviderService.execute(args)

        return IdentifyDataFromProvider(identified_objects=len(object_list),
                                        rdf_dump_url=rdf_file.url)


class IdentifySchemaAndDataFromProvider(graphene.Mutation):
    identified_objects = graphene.Int()
    rdf_dump_url = graphene.String()

    class Arguments:
        provider_name = graphene.String()
        endpoint = graphene.String()

    @login_required
    def mutate(self, info, provider_name, endpoint):
        args = locals()
        [args.pop(x) for x in ["info", "self", "args"]]
        args["user_pk"] = info.context.user.pk

        rdf_file, object_list = IdentifySchemaAndDataFromProviderService.execute(
            args)

        return IdentifyDataFromProvider(identified_objects=len(object_list),
                                        rdf_dump_url=rdf_file.url)


class AddJsonSchema(graphene.Mutation):
    succes = graphene.Boolean()
    objects_added = graphene.Int()
    objects_failed = graphene.Int()

    class Arguments:
        url = graphene.String()
        schema_label = graphene.String()

    @login_required
    def mutate(self, info, url, schema_label):
        args = locals()
        [args.pop(x) for x in ["info", "self", "args"]]
        args["user_pk"] = info.context.user.pk

        added, failed = AddJsonSchemaService.execute(args)

        return AddJsonSchema(
            succes=True,
            objects_added=len(added),
            objects_failed=len(failed))


class AddRdfSchema(graphene.Mutation):
    succes = graphene.Boolean()
    objects_added = graphene.Int()

    class Arguments:
        url = graphene.String()

    @login_required
    def mutate(self, info, url):
        args = locals()
        [args.pop(x) for x in ["info", "self", "args"]]

        AddRdfSchemaService.execute(args)

        return AddRdfSchema(succes=True)


class AddPersonReferenceToBaseObjects(graphene.Mutation):
    objects_added = graphene.Int()

    class Arguments:
        schema_label = graphene.String()

    @login_required
    def mutate(self, info, schema_label):
        args = locals()
        [args.pop(x) for x in ["info", "self", "args"]]

        objects = AddPersonReferenceToBaseObjectsService.execute(args)

        return AddPersonReferenceToBaseObjects(objects_added=len(objects))


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
    identify_data = IdentifyDataFromFile.Field()
    export_schema = ExportSchema.Field()
    add_person_reference = AddPersonReferenceToBaseObjects.Field()
    identify_data_from_provider = IdentifyDataFromProvider.Field()
    identify_data_from_file = IdentifyDataFromFile.Field()
    identify_schema_from_provider = IdentifySchemaFromProvider.Field()
    identify_schema_from_file = IdentifySchemaFromFile.Field()

    identify_schema_and_data_from_provider = IdentifySchemaAndDataFromProvider.Field()
    # identify_schema_and_data_from_file = IdentifySchemaAndDataFromFile.Field()
