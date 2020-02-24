from rest_framework import serializers

from dataproviders.models import DataProvider, OauthConfig, HttpConfig, Endpoint
from dataproviders.serializers.EndpointSerializer import EndpointSerializer
from dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
from dataproviders.serializers.OauthConfigSerializer import OauthConfigSerializer


class DataProviderSerializer(serializers.ModelSerializer):
    oauth_config = OauthConfigSerializer(required=False, allow_null=True)
    http_config = HttpConfigSerializer(required=False, allow_null=True)
    endpoints = EndpointSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = DataProvider
        exclude = ["id"]

    def create(self, validated_data):
        oauth_config = validated_data.pop("oauth_config", None)
        http_config = validated_data.pop("http_config", None)
        endpoints = validated_data.pop("endpoints", None)
        dp = self.Meta.model.objects.create(**validated_data)
        rel_objs = {}
        if oauth_config:
            oauth_config = OauthConfig.objects.create(**oauth_config, data_provider=dp)
            rel_objs["oauth_config"] = oauth_config
        if http_config:
            http_config = HttpConfig.objects.create(**http_config, data_provider=dp)
            rel_objs["http_config"] = http_config
        if endpoints:
            endpoints = [Endpoint.objects.create(**endpoint, data_provider=dp) for endpoint in endpoints]
            rel_objs["endpoints"] = endpoints
        return dp
