import os
import shutil
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User
from MetaDataApi.settings import MEDIA_ROOT


from MetaDataApi.users.schema import UserType
from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation
from MetaDataApi.metadata.services.rdfs_service import RdfService
from MetaDataApi.metadata.services.json_schema_service import JsonSchemaService
from MetaDataApi.metadata.services.schema_identification import SchemaIdentification


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
        schema = graphene.String()

    def mutate(self, info, schema):
        if schema == "all":
            schemas = Schema.objects.all()
            [schema.delete() for schema in schemas]

            try:
                media_schema_folder = os.path.join(MEDIA_ROOT, "schemas")
                # delete all files in media/schemas folder
                shutil.rmtree(media_schema_folder)
                os.makedirs(media_schema_folder)
            except:
                print("does not work on AWS")
        else:
            schema = Schema.objects.get(url=schema)
            schema.delete()

        return DeleteSchema(success=True)


class ExportSchema(graphene.Mutation):
    schema_file = graphene.String()
    visualization_url = graphene.String()

    class Arguments:
        schema_name = graphene.String()

    def mutate(self, info, schema_name):
        service = RdfService()
        outfilename = "./schemas/rdf/created/" + schema_name + ".ttl"

        schema_file_url = service.export_schema_from_db(schema_name)

        return ExportSchema(
            schema_file=schema_file_url,
            visualization_url="http://visualdataweb.de/webvowl/#iri=" + schema_file_url)


class IdentifyData(graphene.Mutation):
    modified_data = graphene.String()

    class Arguments:
        input_data = graphene.String()

    # @login_required
    def mutate(self, info, input_data):
        identify = SchemaIdentification()

        modified_data = identify.identify_data(input_data)

        return IdentifyData(modified_data=modified_data)


class AddJsonSchema(graphene.Mutation):
    succes = graphene.Boolean()
    objects_added = graphene.Int()

    class Arguments:
        url = graphene.String()
        name = graphene.String()

    # @login_required
    def mutate(self, info, url, name):
        service = JsonSchemaService()
        if url == "openMHealth":
            try:

                import threading
                task = service.write_to_db_baseschema
                thr = threading.Thread(target=task)
                thr.start()  # Will run

            except Exception as e:
                raise GraphQLError(e)
        else:
            try:
                service.load_json_schema(url, name)
            except Exception as e:
                raise GraphQLError(str(e))

        return AddRdfSchema(succes=True)


class AddRdfSchema(graphene.Mutation):
    succes = graphene.Boolean()
    objects_added = graphene.Int()

    class Arguments:
        url = graphene.String()

    # @login_required
    def mutate(self, info, url):
        service = RdfService()
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

    # # @login_required
    # # schemas

    def resolve_schema(self, info):
        return Schema.objects.first()

    def resolve_all_schema(self, info):
        return Schema.objects.all()

    # objects
    def resolve_object(self, info):
        return Object.objects.first()

    def resolve_all_objects(self, info):
        return Object.objects.all()

    # attributes
    def resolve_attribute(self, info):
        return Attribute.objects.first()

    def resolve_all_attributes(self, info):
        return Attribute.objects.all()

    # object relations
    def resolve_object_relation(self, info):
        return ObjectRelation.objects.first()

    def resolve_all_object_relations(self, info):
        return ObjectRelation.objects.all()


class Mutation(graphene.ObjectType):
    add_rdf_schema = AddRdfSchema.Field()
    add_json_schema = AddJsonSchema.Field()
    delete_schema = DeleteSchema.Field()
    identify_data = IdentifyData.Field()
    export_schema = ExportSchema.Field()
