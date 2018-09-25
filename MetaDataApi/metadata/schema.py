import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User


from MetaDataApi.users.schema import UserType
from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation
from MetaDataApi.metadata.services.rdf import rdfService


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
        else:
            schema = Schema.objects.get(url=schema)
            Schema.delete()

        return DeleteSchema(success=True)


class AddRdfSchema(graphene.Mutation):
    succes = graphene.Boolean()
    objects_added = graphene.Int()

    class Arguments:
        url = graphene.String()

    # @login_required
    def mutate(self, info, url):
        service = rdfService()
        if url == "baseschema":
            try:
                service.create_default_schemas()
            except Exception as e:
                raise GraphQLError(str(e))
        else:
            try:
                service.rdfs_upload(url)
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
    delete_schema = DeleteSchema.Field()
