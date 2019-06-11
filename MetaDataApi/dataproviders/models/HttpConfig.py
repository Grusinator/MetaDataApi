from django.db import models

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.metadata.utils import JsonUtils


class HttpConfig(models.Model):
    data_provider = models.OneToOneField(DataProvider, related_name="http_config", on_delete=models.CASCADE)
    header = models.TextField()
    url_encoded_params = models.TextField()
    body_type = models.TextField()
    body_content = models.TextField()
    request_type = models.TextField()

    # http_config = models.ManyToOneRel("HttpConfig")
    # oauth_config = models.ManyToOneRel("OauthConfig")

    def build_header(self):
        try:
            return dict(JsonUtils.loads(self.header))
        except Exception as e:
            return dict()
