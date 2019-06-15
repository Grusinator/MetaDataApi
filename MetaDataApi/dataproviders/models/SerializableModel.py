from django.db.models import ForeignKey, OneToOneField
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor, ReverseManyToOneDescriptor
from rest_framework.serializers import ModelSerializer

from MetaDataApi.metadata.utils import JsonUtils
from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType


class SerializableModel:
    model_relations = (ForeignKey, OneToOneField,)
    model_descriptors = (ReverseOneToOneDescriptor, ReverseManyToOneDescriptor)
    DEPTH_INFINITE = 999999

    def serialize(self, depth: int = DEPTH_INFINITE, exclude: tuple = ()):
        Serializer = type(self).build_serializer(depth, exclude)
        data = Serializer(self).data
        return JsonUtils.dump_and_load(data)

    @classmethod
    def deserialize(cls, data: JsonType, depth: int = DEPTH_INFINITE, exclude: tuple = ()):
        Serializer = cls.build_serializer(depth, exclude)
        serializer = Serializer(data=data)
        if not serializer.is_valid():
            raise Exception("could not deserialize")
        return cls.objects.create(serializer.validated_data)

    @classmethod
    def build_serializer(cls, depth: int = DEPTH_INFINITE, exclude: tuple = ()):
        properties = cls.build_properties(depth, exclude)
        return type(cls.__name__ + "Serializer", (ModelSerializer,), properties)

    @classmethod
    def build_properties(cls, depth, exclude) -> dict:
        properties = {"Meta": cls.build_meta_class()}
        if depth:
            depth = cls.adjust_depth(depth)
            properties.update(cls.get_relation_serializers(depth, exclude))
        return properties

    @classmethod
    def get_relation_serializers(cls, depth, exclude) -> dict:
        model_relation_names = cls.get_all_model_relations_names()
        model_relation_names = set(model_relation_names) - set(exclude)
        return {name: cls.build_serializer_from_property_name(name, depth) for name in model_relation_names}

    @classmethod
    def build_serializer_from_property_name(cls, name, depth):
        foreignkey_object = cls.get_related_object_by_property_name(name)
        return foreignkey_object.build_serializer(depth)

    @classmethod
    def get_related_object_by_property_name(cls, property_name):
        return cls._meta.get_field(property_name).related_model

    @classmethod
    def build_meta_class(cls):
        return type(
            "Meta", (),
            {
                "model": cls,
                "exclude": ["id"] + cls.get_all_model_relations_names()}
        )

    @classmethod
    def get_all_model_relations_names(cls) -> list:
        # TODO remove this _set when this has been handled
        return [k for k, v in cls.__dict__.items() if isinstance(v, cls.model_descriptors) and "_set" not in k]

    @classmethod
    def adjust_depth(cls, depth):
        if depth == cls.DEPTH_INFINITE:
            return depth
        else:
            return depth - 1 if depth > 0 else 0
