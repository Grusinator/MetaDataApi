from django.db.models import ForeignKey, OneToOneField
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor, ReverseManyToOneDescriptor
from rest_framework.serializers import ModelSerializer


class SerializableModel:
    model_relations = (ForeignKey, OneToOneField,)
    model_descriptors = (ReverseOneToOneDescriptor, ReverseManyToOneDescriptor)
    DEPTH_INFINITE = 999999

    def serialize(self):
        return

    def deserialize(self):
        return

    @classmethod
    def build_serializer(cls, depth: int = DEPTH_INFINITE, ignore: tuple = ()):
        properties = cls.build_properties(depth, ignore)
        return type(cls.__name__ + "Serializer", (ModelSerializer,), properties)

    @classmethod
    def build_properties(cls, depth, ignore) -> dict:
        properties = {"Meta": cls.build_meta_class()}
        if depth:
            depth = cls.adjust_depth(depth)
            properties.update(cls.get_relation_serializers(depth, ignore))
        return properties

    @classmethod
    def get_relation_serializers(cls, depth, ignore) -> dict:
        model_relation_names = cls.get_all_model_relations_names()
        model_relation_names = set(model_relation_names) - set(ignore)
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
                "ignore": ["id"] + cls.get_all_model_relations_names()}
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
