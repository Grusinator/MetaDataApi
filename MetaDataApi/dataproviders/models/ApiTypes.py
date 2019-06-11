from MetaDataApi.metadata.utils.django_model_utils.DjangoModelEnum import DjangoModelEnum


class ApiTypes(DjangoModelEnum):
    OAUTH_REST = "OauthRest"
    OAUTH_GRAPHQL = "OauthGraphql"
    TOKEN_REST = "TokenRest"
