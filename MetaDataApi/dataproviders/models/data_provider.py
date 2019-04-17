import json
from enum import Enum
from urllib import parse

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse

from MetaDataApi.metadata.models import Schema
from MetaDataApi.metadata.rdfs_models import RdfsDataProvider

SItems = RdfsDataProvider.SchemaItems

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
        null=True, blank=True,
        related_name="db_data_provider"
    )

    def get_internal_view_url(self):
        return reverse('provider_detail', args=[str(self.provider_name)])

    def get_webvowl_url(self):
        schema = self.get_schema_for_provider()
        return "http://visualdataweb.de/webvowl/#iri=" + schema.rdfs_file.url

    def __str__(self):
        return "%s - %s" % (self.provider_name, self.api_endpoint)

    def save(self, *args, **kwargs):
        if not self.data_provider_instance:
            self.data_provider_instance = RdfsDataProvider.create_data_provider(
                str(self.provider_name))

        if not Schema.exists_by_label(str(self.provider_name)):
            Schema.create_new_empty_schema(self.provider_name)

        existing_endpoints = RdfsDataProvider.get_all_endpoints(self.data_provider_instance)

        for endpoint in json.loads(self.rest_endpoints_list):
            endpoint_url = endpoint["url"]
            endpoint_name = endpoint["name"]
            rdf_endpoint = RdfsDataProvider.find_endpoint_with_name(existing_endpoints, endpoint_name)
            if rdf_endpoint:
                self.update_endpoint_url(endpoint_url, rdf_endpoint)
            else:
                RdfsDataProvider.create_endpoint_to_data_provider(
                    self.data_provider_instance,
                    endpoint_url,
                    endpoint_name
                )
        super(DataProvider, self).save(*args, **kwargs)

    @staticmethod
    def update_endpoint_url(endpoint_url, rdf_endpoint):
        rdf_endpoint_url = rdf_endpoint.get_att_inst(SItems.endpoint_template_url)
        if rdf_endpoint_url is not endpoint_url:
            rdf_endpoint_url.value = endpoint_url
            rdf_endpoint_url.save()

    @classmethod
    def exists(cls, provider_name):
        try:
            return cls.objects.get(provider_name=provider_name)
        except ObjectDoesNotExist:
            return None

    def do_endpoint_exist(self, endpoint):
        if endpoint not in self.rest_endpoints_list:
            print("warning: This is not a known %s endpoint - \"%s\" " %
                  (self.provider_name, endpoint))
            return True
        else:
            return False

    def get_schema_for_provider(self):
        return Schema.objects.get(label=self.provider_name)

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
