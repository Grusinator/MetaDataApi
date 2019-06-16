from rest_framework import serializers

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.dataproviders.serializers.EndpointSerializer import EndpointSerializer
from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
from MetaDataApi.dataproviders.serializers.OauthConfigSerializer import OauthConfigSerializer


class DataProviderSerializer(serializers.ModelSerializer):
    oauth_config = OauthConfigSerializer()
    http_config = HttpConfigSerializer()
    endpoints = EndpointSerializer(many=True)

    class Meta:
        model = DataProvider
        exclude = ["id"]
