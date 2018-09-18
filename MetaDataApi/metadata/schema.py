import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from graphql.error import GraphQLError

from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User


from MetaDataApi.users.schema import UserType
from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation

#class SchemaExportType(DjangoObjectType):
#    class Meta:
#        response

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

class ObjectRelationNode(DjangoObjectType):
    class Meta:
        model = ObjectRelation
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

    object_relation = graphene.relay.Node.Field(ObjectRelationNode)
    all_object_relations = DjangoFilterConnectionField(ObjectRelationNode)

    #@login_required

    #schemas
    def resolve_schema(self, info):
        return Schema.objects.first()

    def resolve_all_schema(self, info):
        return Schema.Objects.All()

    #objects
    def resolve_object(self, info): 
        return Object.objects.first()

    def resolve_all_objects(self, info): 
        return Object.objects.All()

    #attributes
    def resolve_attribute(self, info):
        return Attribute.objects.first()
    
    def resolve_all_attributes(self, info):
        return Attribute.objects.All()

    #object relations
    def resolve_object_relation(self, info): 
        return ObjectRelation.objects.first()

    def resolve_all_object_relations(self, info): 
        return ObjectRelation.objects.All()



class Mutation(graphene.ObjectType):
    pass

