from rest_framework import serializers

from dataproviders.models import Endpoint


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        exclude = ["id", "data_provider"]
