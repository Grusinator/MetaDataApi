from rest_framework.serializers import ModelSerializer, JSONField

from MetaDataApi.dataproviders.models.HttpConfig import HttpConfig


class HttpConfigSerializer(ModelSerializer):
    header = JSONField()
    url_encoded_params = JSONField()

    class Meta:
        model = HttpConfig
        fields = ["url_encoded_params", "header"]

    @classmethod
    def build_from_metaclass(cls):
        properties = cls.build_properties()
        return type("MetaHttpConfigSerializer", (ModelSerializer,), properties)

    @classmethod
    def build_properties(cls):
        properties = {
            "Meta": cls.build_nested_meta_class(),
            "header": JSONField(),
            "url_encoded_params": JSONField()
        }
        return properties

    @classmethod
    def build_nested_meta_class(cls):
        properties = {
            "model": HttpConfig,
            "fields": ["header", "url_encoded_params"]
        }
        return type("Meta", (), properties)
