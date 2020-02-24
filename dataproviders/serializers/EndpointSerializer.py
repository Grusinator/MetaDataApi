from rest_framework import serializers

from dataproviders.models import Endpoint


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        exclude = ["id", "data_provider"]

    def create(self, validated_data):
        validated_data.pop("data_fetches")
        return self.Meta.model.objects.create(**validated_data)
