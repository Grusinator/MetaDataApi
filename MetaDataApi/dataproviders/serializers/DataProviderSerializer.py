from rest_framework import serializers

from MetaDataApi.dataproviders.models import DataProvider


class DataProviderSerializer(serializers.ModelSerializer):
    # oauth_config = OauthConfigSerializer()
    # http_config = HttpConfigSerializer()
    # endpoints = EndpointSerializer(many=True)

    class Meta:
        model = DataProvider
        exclude = ["id"]
