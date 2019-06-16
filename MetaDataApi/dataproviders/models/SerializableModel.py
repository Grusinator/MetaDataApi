import logging

from django.db.models import TextField, IntegerField, FloatField, BooleanField, ForeignKey, OneToOneField, ManyToOneRel, \
    OneToOneRel
from rest_framework.serializers import ModelSerializer

from MetaDataApi.metadata.utils import JsonUtils
from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType

logger = logging.getLogger(__name__)


class SerializableModel:
    many_to_one_relation_types = (ForeignKey, ManyToOneRel)
    one_to_one_relation_types = (OneToOneField, OneToOneRel)
    relation_types = many_to_one_relation_types + one_to_one_relation_types
    attribute_types = (TextField, IntegerField, FloatField, BooleanField)
    DEPTH_INFINITE = 999999
    MODEL = "model"
    META = "Meta"
    FIELDS = "fields"

    def serialize(self, depth: int = DEPTH_INFINITE, exclude: tuple = ()):
        Serializer = type(self).build_serializer(depth, exclude)
        data = Serializer(self).data
        return JsonUtils.dump_and_load(data)

    @classmethod
    def deserialize(cls, data: JsonType, depth: int = DEPTH_INFINITE, exclude: tuple = ()):
        Serializer = cls.build_serializer(depth, exclude)
        serializer = Serializer(data=data)
        if not serializer.is_valid():
            raise Exception(f"could not deserialize, due to error: {serializer.default_errors}")
        return serializer.validated_data
        # return cls.objects.create(serializer.validated_data)

    @classmethod
    def build_serializer(cls, depth: int = DEPTH_INFINITE, exclude: tuple = ()):
        properties = cls.build_properties(depth, exclude)
        return type(cls.__name__ + "Serializer", (ModelSerializer,), properties)

    @classmethod
    def build_properties(cls, depth, exclude) -> dict:
        properties = {cls.META: cls.build_meta_class(exclude)}
        if depth:
            depth = cls.adjust_depth(depth)
            properties = cls.add_relations_to_properties(properties, depth, exclude)
        return properties

    @classmethod
    def build_relation_serializers(cls, relation_names, depth) -> dict:
        return {name: cls.try_build_relation_serializer_instance(name, depth) for name in relation_names}

    @classmethod
    def try_build_relation_serializer_instance(cls, property_name, depth):
        try:
            foreignkey_object = cls.get_related_object_by_property_name(property_name)
            Serializer = foreignkey_object.build_serializer(depth)
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
    def build_meta_class(cls, exclude):
        meta_properties = {
            cls.MODEL: cls,
            cls.FIELDS: cls.get_all_attribute_names(exclude)
        }
        return type(cls.META, (), meta_properties)

    @classmethod
    def get_all_model_relations_names(cls, exclude: list = ()) -> list:
        names = cls.get_all_field_names_of_type(cls.relation_types)
        # TODO remove this _set when this has been handled
        return [name for name in names if ("_set" not in name) and (name not in exclude)]

    @classmethod
    def get_all_attribute_names(cls, exclude: list):
        names = cls.get_all_field_names_of_type(cls.attribute_types)
        return [name for name in names if name not in exclude]

    @classmethod
    def get_all_field_names_of_type(cls, types) -> list:
        return [field.name for field in cls._meta.get_fields() if isinstance(field, types)]

    @classmethod
    def adjust_depth(cls, depth):
        if depth == cls.DEPTH_INFINITE:
            return depth
        else:
            return depth - 1 if depth > 0 else 0

    @classmethod
    def add_relations_to_properties(cls, properties, depth, exclude):
        relation_names = cls.get_all_model_relations_names(exclude)
        properties[cls.META].fields += relation_names
        properties.update(cls.build_relation_serializers(relation_names, depth))
        return properties
