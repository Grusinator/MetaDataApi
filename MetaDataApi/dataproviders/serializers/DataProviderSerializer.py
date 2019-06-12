from rest_framework import serializers

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.dataproviders.serializers.HttpConfigSerializer import HttpConfigSerializer
from MetaDataApi.dataproviders.serializers.OauthConfigSerializer import OauthConfigSerializer


class DataProviderSerializer(serializers.ModelSerializer):
    oauth_config = OauthConfigSerializer()
    http_config = HttpConfigSerializer()

    class Meta:
        model = DataProvider
