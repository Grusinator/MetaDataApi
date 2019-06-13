from rest_framework import serializers

from MetaDataApi.dataproviders.models.HttpConfig import HttpConfig


class HttpConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = HttpConfig
        exclude = ["id", "data_provider"]
