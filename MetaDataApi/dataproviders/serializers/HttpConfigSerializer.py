from rest_framework import serializers

from MetaDataApi.dataproviders.models.HttpConfig import HttpConfig


class HttpConfigSerializer(serializers.ModelSerializer):
    header = serializers.JSONField()
    url_encoded_params = serializers.JSONField()
    class Meta:
        model = HttpConfig
        fields = ["header", "url_encoded_params"]
