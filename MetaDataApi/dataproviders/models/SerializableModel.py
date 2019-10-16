import logging

from django.db.models import TextField, IntegerField, FloatField, BooleanField, ForeignKey, OneToOneField, ManyToOneRel, \
    OneToOneRel
from jsonfield import JSONField
from rest_framework.serializers import ModelSerializer, JSONField as JSONSerializerField

from MetaDataApi.dataproviders.models.SerializableModelFilter import SerializableModelFilter
from MetaDataApi.metadata.utils import JsonUtils
from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType

logger = logging.getLogger(__name__)


class SerializableModel:
    many_to_one_relation_types = (ForeignKey, ManyToOneRel)
    one_to_one_relation_types = (OneToOneField, OneToOneRel)
    relation_types = many_to_one_relation_types + one_to_one_relation_types
    attribute_types = (TextField, IntegerField, FloatField, BooleanField, JSONField)

    MODEL = "model"
    META = "Meta"
    FIELDS = "fields"

    CUSTOM_FIELDS = {
        JSONField: JSONSerializerField,
    }

    def serialize(self, max_depth: int = SerializableModelFilter.DEPTH_INFINITE, exclude: tuple = ()):
        filter = SerializableModelFilter(max_depth, exclude_labels=exclude)
        Serializer = type(self).build_serializer(filter)
        data = Serializer(self).data
        return JsonUtils.dump_and_load(data)

    @classmethod
    def deserialize(cls, data: JsonType, max_depth: int = SerializableModelFilter.DEPTH_INFINITE, exclude: tuple = ()):
        filter = SerializableModelFilter(max_depth=max_depth, exclude_labels=exclude)
        validated_data = cls.deserialize_to_validated_data(data, filter)
        # cls.create_object_from_validated_data(validated_data)
        return validated_data

    @classmethod
    def deserialize_to_validated_data(cls, data, filter: SerializableModelFilter):
        Serializer = cls.build_serializer(filter)
        serializer = Serializer(data=data)
        if not serializer.is_valid():
            raise Exception(f"could not deserialize, due to error: {serializer.errors}")
        return serializer.validated_data

    @classmethod
    def create_object_from_validated_data(cls, validated_data):
        return cls(**validated_data)

    @classmethod
    def build_serializer(cls, filter: SerializableModelFilter):
        properties = cls.build_properties(filter)
        return type(cls.__name__ + "Serializer", (ModelSerializer,), properties)

    @classmethod
    def build_properties(cls, filter: SerializableModelFilter) -> dict:
        properties = {cls.META: cls.build_meta_class(filter)}
        custom_field_properties = cls.build_custom_field_properties(filter)
        properties.update(custom_field_properties)
        properties = cls.add_relations_to_properties(properties, filter)
        return properties

    @classmethod
    def build_relation_serializers(cls, relation_names, filter) -> dict:
        return {name: cls.try_build_relation_serializer_instance(name, filter) for name in relation_names}

    @classmethod
    def try_build_relation_serializer_instance(cls, property_name, filter):
        try:
            foreignkey_object = cls.get_related_object_by_property_name(property_name)
            Serializer = foreignkey_object.build_serializer(filter)
            return Serializer(many=cls.is_related_object_many(property_name))
        except Exception as e:
            logger.warning(f"could not create related serializer object with name: {property_name}")

    @classmethod
    def is_related_object_many(cls, property_name):
        return type(cls._meta.get_field(property_name)) in cls.many_to_one_relation_types

    @classmethod
    def get_related_object_by_property_name(cls, property_name):
        return cls._meta.get_field(property_name).related_model

    @classmethod
    def build_meta_class(cls, filter):
        meta_properties = {
            cls.MODEL: cls,
            cls.FIELDS: cls.get_all_attribute_names(filter)
        }
        return type(cls.META, (), meta_properties)

    @classmethod
    def get_all_model_relations_names(cls, filter) -> list:
        names = cls.get_all_field_names_of_type(cls.relation_types)
        # TODO remove this _set when this has been handled
        return [name for name in names if ("_set" not in name) and (name not in filter.exclude_labels)]

    @classmethod
    def get_all_attribute_names(cls, filter):
        names = cls.get_all_field_names_of_type(cls.attribute_types)
        return [name for name in names if name not in filter.exclude_labels]

    @classmethod
    def get_all_field_names_of_type(cls, types) -> list:
        return [field.name for field in cls._meta.get_fields() if isinstance(field, types)]

    @classmethod
    def add_relations_to_properties(cls, properties, filter):

        relation_names = cls.get_all_model_relations_names(filter)
        properties[cls.META].fields += relation_names
        properties.update(cls.build_relation_serializers(relation_names, filter))
        return properties

    @classmethod
    def build_custom_field_properties(cls, filter):
        custom_field_properties = {}
        for ModelField, SerializerField in cls.CUSTOM_FIELDS.items():
            names = cls.get_all_field_names_of_type(ModelField)
            custom_field_properties.update(
                {name: SerializerField() for name in names if name not in filter.exclude_labels})
        return custom_field_properties
