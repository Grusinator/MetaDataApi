from rest_framework import serializers

from dataproviders.models import DataProvider
from dataproviders.serializers.EndpointSerializer import EndpointSerializer
from dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
from dataproviders.serializers.OauthConfigSerializer import OauthConfigSerializer


class DataProviderSerializer(serializers.ModelSerializer):
    oauth_config = OauthConfigSerializer(required=False)
    http_config = HttpConfigSerializer(required=False)
    endpoints = EndpointSerializer(many=True, required=False)

    class Meta:
        model = DataProvider
        exclude = ["id"]
