from urllib import parse

from django.db import models

from MetaDataApi import settings
from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.dataproviders.models.SerializableModel import SerializableModel
from MetaDataApi.metadata.utils import JsonUtils


class OauthConfig(models.Model, SerializableModel):
    data_provider = models.OneToOneField(DataProvider, related_name="oauth_config", on_delete=models.CASCADE)
    authorize_url = models.TextField()
    access_token_url = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scope = models.TextField()

    def __str__(self):
        return f"OAuth2:{self.data_provider.name}"

    class Meta:
        app_label = 'dataproviders'

    def build_auth_url(self, user_id: int):
        user_id = str(user_id) or "AnonomousUser"
        state = f"{self.data_provider.provider_name}:{user_id}"

        args = {
            "client_id": self.client_id,
            "redirect_uri": settings.OAUTH_REDIRECT_URI,
            "nounce": "sdfkjlhasdfdhfas",
            "response_type": "code",
            "response_mode": "form_post",
            "state": state,
            "scope": self.build_scopes_string()
        }

        args_string = parse.urlencode(tuple(args.items()))

        url = f"{self.authorize_url}?{args_string}"
        return url

    def build_scopes_string(self):
        if self.scope:
            scopes = JsonUtils.loads(str(self.scope))
            return " ".join(scopes)
