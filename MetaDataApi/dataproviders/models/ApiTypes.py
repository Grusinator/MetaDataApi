from MetaDataApi.metadata.utils.django_model_utils.DjangoModelEnum import DjangoModelEnum


class ApiTypes(DjangoModelEnum):
    OauthRest = "Oauth2-rest"
    OauthGraphql = "Oauth2-graphql"
    TokenRest = "Token-rest"
