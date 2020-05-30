from MetaDataApi.utils.django_utils.django_model_enum import DjangoModelEnum


class AuthType(DjangoModelEnum):
    TOKEN = "token"
    OAUTH2 = "oauth2"
    NONE = None
