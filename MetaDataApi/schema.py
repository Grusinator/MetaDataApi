import MetaDataApi.metadata.schema
import MetaDataApi.users.schema
import graphene
import graphql_jwt



from graphene_django.debug import DjangoDebug


class Query(
    MetaDataApi.users.schema.Query, 
    MetaDataApi.metadata.schema.Query, 
    graphene.ObjectType):

    debug = graphene.Field(DjangoDebug, name='__debug')

class Mutation(
    MetaDataApi.users.schema.Mutation, 
    MetaDataApi.metadata.schema.Mutation, 
    graphene.ObjectType):
    
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    debug = graphene.Field(DjangoDebug, name='__debug')

schema = graphene.Schema(query=Query, mutation=Mutation)
