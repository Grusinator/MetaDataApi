import graphene
from graphene_django.filter import DjangoFilterConnectionField
import meta_schema
import instances_schema


class Query(meta_schema.Query, instances_schema.Query):
    pass


class Mutation(meta_schema.Mutation, instances_schema.Mutation):
    pass
