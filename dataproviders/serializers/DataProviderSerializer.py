from rest_framework import serializers

from dataproviders.models import DataProvider
from dataproviders.serializers.EndpointSerializer import EndpointSerializer
from dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
from dataproviders.serializers.OauthConfigSerializer import OauthConfigSerializer


class DataProviderSerializer(serializers.ModelSerializer):
    oauth_config = OauthConfigSerializer()
    http_config = HttpConfigSerializer()
    endpoints = EndpointSerializer(many=True)

    class Meta:
        model = DataProvider
        exclude = ["id"]
