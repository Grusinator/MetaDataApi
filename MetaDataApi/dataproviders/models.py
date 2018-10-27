from django.db import models

# Create your models here.


class ThirdPartyDataProvider(models.Model):
    provider_name = models.TextField(unique=True)
    api_type = models.TextField(
        choices=["Oauth2-rest", "Oauth2-graphql", "Token-rest"])
    api_endpoint = models.TextField()
    authorize_url = models.TextField()
    access_token_url = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scope = models.TextField()
    redirect_uri = models.TextField()
    rest_endpoints_list = models.TextField()
    json_schema_file_url = models.TextField(null=False, blank=False)

    def __str__(self):
        return "%s - %s" % (self.provider_name, self.api_endpoint)

    class Meta:
        app_label = 'dataproviders'
