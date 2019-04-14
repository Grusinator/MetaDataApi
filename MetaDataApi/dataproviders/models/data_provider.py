import json
from enum import Enum
from urllib import parse

from django.db import models

# Create your models here.
from MetaDataApi.metadata.rdf_models import RdfDataProvider
from MetaDataApi.settings import OAUTH_REDIRECT_URI


class ApiTypes(Enum):
    OauthRest = "Oauth2-rest"
    OauthGraphql = "Oauth2-graphql"
    TokenRest = "Token-rest"


class DataProvider(models.Model):
    provider_name = models.TextField(unique=True)
    api_type = models.TextField(
        choices=[(type.value, type.name) for type in ApiTypes])
    api_endpoint = models.TextField()
    authorize_url = models.TextField()
    access_token_url = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scope = models.TextField()
    rest_endpoints_list = models.TextField()
    json_schema_file_url = models.TextField(null=True, blank=True)
    data_provider_instance = models.ForeignKey(
        "metadata.ObjectInstance",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        return "%s - %s" % (self.provider_name, self.api_endpoint)

    def save(self, *args, **kwargs):
        if not self.data_provider_instance:
            self.data_provider_instance = RdfDataProvider.create_data_provider(
                str(self.provider_name))

        super(DataProvider, self).save(*args, **kwargs)

    @classmethod
    def exists(cls, provider_name):
        return cls.objects.get(provider_name=provider_name)

    def do_endpoint_exist(self, endpoint):
        if endpoint not in self.rest_endpoints_list:
            print("warning: This is not a known %s endpoint - \"%s\" " %
                  (self.provider_name, endpoint))
            return True
        else:
            return False

    def build_auth_url(self, logged_in_user_id=None):

        state = "%s:%s" % (self.provider_name,
                           logged_in_user_id or "AnonomousUser")

        try:
            scopes = json.loads(self.scope)
            scopes = " ".join(scopes)
        except:
            scopes = ""

        args = {
            "client_id": self.client_id,
            "redirect_uri": OAUTH_REDIRECT_URI,
            "scope": scopes,
            "nounce": "sdfkjlhasdfdhfas",
            "response_type": "code",
            "response_mode": "form_post",
            "state": state,
        }

        if any([not bool(value.strip(" ")) for value in args.values()]):
            return ""

        args_string = parse.urlencode(tuple(args.items()))

        url = "%s?%s" % (self.authorize_url, args_string)

        return url

    class Meta:
        app_label = 'dataproviders'
