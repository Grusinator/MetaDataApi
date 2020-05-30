from MetaDataApi.utils.django_utils.django_model_enum import DjangoModelEnum


class ApiType(DjangoModelEnum):
    REST = "rest"
    GRAPHQL = "graphql"
