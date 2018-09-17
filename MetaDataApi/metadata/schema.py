import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User


from MetaDataApi.users.schema import UserType
from MetaDataApi.metadata.models import Schema, Object, Attribute



class SchemaNode(DjangoObjectType):
    class Meta:
        model = Schema
        filter_fields = ['name', 'description']
        interfaces = (graphene.relay.Node, )

class ObjectNode(DjangoObjectType):
    class Meta:
        model = Object
        filter_fields = ['name', 'description']
        interfaces = (graphene.relay.Node, )

class AttributeNode(DjangoObjectType):
    class Meta:
        model = Attribute
        filter_fields = ['name',]
        interfaces = (graphene.relay.Node, )

# wrap all queries and mutations
class Query(graphene.ObjectType):
    schema = graphene.relay.Node.Field(SchemaNode)
    all_schemas = DjangoFilterConnectionField(SchemaNode)

    object = graphene.relay.Node.Field(ObjectNode)
    all_objects = DjangoFilterConnectionField(ObjectNode)

    attribute = graphene.relay.Node.Field(AttributeNode)
    all_attributes = DjangoFilterConnectionField(AttributeNode)

    #schema = graphene.Field(SchemaNode)
    #object = graphene.Field(ObjectNode)
    #schema = graphene.Field(AttributeNode)


    #@login_required
    def resolve_schema(self, info):

        schema = Schema.objects.first()
        return schema

    def resolve_all_schema(self, info):
        return Schema.Objects.All()

    def resolve_object(self, info): 
        return Object.objects.first()

    def resolve_attribute(self, info):
        return Attribute.objects.first()



class Mutation(graphene.ObjectType):
    pass

