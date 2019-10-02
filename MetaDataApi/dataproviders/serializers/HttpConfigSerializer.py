from rest_framework.serializers import ModelSerializer, JSONField

from MetaDataApi.dataproviders.models.HttpConfig import HttpConfig


class HttpConfigSerializer(ModelSerializer):
    header = JSONField()
    url_encoded_params = JSONField()

    class Meta:
        model = HttpConfig
        fields = ["header", "url_encoded_params"]

    @classmethod
    def build_from_metaclass(cls):
        properties = {
            "Meta": cls.build_nested_meta_class(),
            "header": JSONField(),
            "url_encoded_params" : JSONField()

        }
        return type("MetaHttpConfigSerializer", (ModelSerializer,), properties)

    @classmethod
    def build_nested_meta_class(cls):
        properties = {
            "model": HttpConfig,
            "fields": ["header", "url_encoded_params"]
        }
        return type("Meta", (), properties)

class SomeClass:
    class Meta:
        model = HttpConfig
        fields = ["header", "url_encoded_params"]

    @classmethod
    def build_some_class(cls):
        properties = {
            "Meta": cls.build_Meta_class()
        }
        return type("someclass", (), properties)

    @classmethod
    def build_Meta_class(cls):
        properties = {
            "model": HttpConfig,
            "fields" : ["header", "url_encoded_params"]
        }
        return type("Meta", (), properties)