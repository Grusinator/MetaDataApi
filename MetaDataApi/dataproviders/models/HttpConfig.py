# switch between djongo and postgres Jsonfields
# from djongo.models.json import JSONField
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.dataproviders.models.SerializableModel import SerializableModel
from MetaDataApi.metadata.utils import JsonUtils


class HttpConfig(models.Model, SerializableModel):
    data_provider = models.OneToOneField(DataProvider, related_name="http_config", on_delete=models.CASCADE)
    header = JSONField(encoder=DjangoJSONEncoder, null=True, blank=True)
    url_encoded_params = JSONField(encoder=DjangoJSONEncoder, null=True, blank=True)
    body_type = models.TextField(null=True, blank=True)
    body_content = models.TextField(null=True, blank=True)
    request_type = models.TextField(null=True, blank=True)

    # http_config = models.ManyToOneRel("HttpConfig")
    # oauth_config = models.ManyToOneRel("OauthConfig")

    def build_header(self):
        try:
            return dict(JsonUtils.loads(self.header))
        except Exception as e:
            return dict()
