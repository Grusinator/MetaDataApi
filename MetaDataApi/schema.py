import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug

# import datapoints.schema
# import dataproviders.schema
import users.schema
from dynamic_models.schema import build_dynamic_model_query


class Query(
    users.schema.Query,
    # metadata.schema.schema.Query,
    # datapoints.schema.Query,
    # dataproviders.schema.Query,
    build_dynamic_model_query(),
    graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(
    users.schema.Mutation,
    # metadata.schema.schema.Mutation,
    # MetaDataApi.datapoints.schema.Mutation,
    # dataproviders.schema.Mutation,
    graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
