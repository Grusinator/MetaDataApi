from rest_framework import serializers

from dataproviders.models import OauthConfig


class OauthConfigSerializer(serializers.ModelSerializer):
    scope = serializers.JSONField(required=False)

    class Meta:
        model = OauthConfig
        exclude = ["id", "data_provider"]
