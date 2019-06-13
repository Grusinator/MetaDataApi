from rest_framework import serializers

from MetaDataApi.dataproviders.models import OauthConfig


class OauthConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = OauthConfig
        exclude = ["id", "data_provider"]
