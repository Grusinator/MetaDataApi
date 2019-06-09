from enum import Enum

from django.db import models

from MetaDataApi.dataproviders.models.DataProvider import DataProvider


class ApiTypes(Enum):
    OauthRest = "Oauth2-rest"
    OauthGraphql = "Oauth2-graphql"
    TokenRest = "Token-rest"


class Endpoint(models.Model):
    name = models.TextField()
    url = models.TextField()
    api_type = models.TextField(
        choices=[(type.value, type.name) for type in ApiTypes])
    provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)
