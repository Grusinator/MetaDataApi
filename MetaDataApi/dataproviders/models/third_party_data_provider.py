import json
import urllib

from django.db import models

# Create your models here.
from settings import OAUTH_REDIRECT_URI

api_type_choises = [(x, x) for x in [
    "Oauth2-rest",
    "Oauth2-graphql",
    "Token-rest"]]


class ThirdPartyDataProvider(models.Model):
    provider_name = models.TextField(unique=True)
    api_type = models.TextField(choices=api_type_choises)
    api_endpoint = models.TextField()
    authorize_url = models.TextField()
    access_token_url = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scope = models.TextField()
    rest_endpoints_list = models.TextField()
    json_schema_file_url = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.provider_name, self.api_endpoint)

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

        args_string = urllib.parse.urlencode(tuple(args.items()))

        url = "%s?%s" % (self.authorize_url, args_string)

        return url

    class Meta:
        app_label = 'dataproviders'
