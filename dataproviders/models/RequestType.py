from MetaDataApi.utils.django_model_utils.DjangoModelEnum import DjangoModelEnum


class RequestType(DjangoModelEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    UPDATE = "UPDATE"
