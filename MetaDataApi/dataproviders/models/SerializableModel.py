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

    def serialize(self, max_depth: int = SerializableModelFilter.DEPTH_INFINITE, exclude_labels: tuple = ()):
        filter = SerializableModelFilter(max_depth, exclude_labels=exclude_labels)
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
        serialized_object = serializer.save()
        return serializer.validated_data

    @classmethod
    def create_object_from_validated_data(cls, validated_data):
        # AssertionError: The `.create()` method does not support writable nested fields by default.
        # Write an explicit `.create()` method for serializer `rest_framework.serializers.DataProviderSerializer`,
        # or set `read_only=True` on nested serializer fields.
        # TODO: fix this by adding a create method in the generic serializer

        # https://stackoverflow.com/questions/41394761/the-create-method-does-not-support-writable-nested-fields-by-default
        #     def create(self, validated_data):
        #         order = Order.objects.get(pk=validated_data.pop('event'))
        #         instance = Equipment.objects.create(**validated_data)
        #         Assignment.objects.create(Order=order, Equipment=instance)
        #         return instance
        #
        #     def to_representation(self, instance):
        #         representation = super(EquipmentSerializer, self).to_representation(instance)
        #         representation['assigment'] = AssignmentSerializer(instance.assigment_set.all(), many=True).data
        #         return representation

        return cls(**validated_data)

    @classmethod
    def build_serializer(cls, filter: SerializableModelFilter):
        properties = cls.build_properties(filter)
        return type(cls.__name__ + "Serializer", (ModelSerializer,), properties)

    @classmethod
    def build_properties(cls, filter: SerializableModelFilter) -> dict:
        # each property must contain the serializer class for any related object so it is here the recursive filtering
        # is handled
        properties = {cls.META: cls.build_meta_class(filter)}
        custom_field_properties = cls.build_custom_field_properties(filter)
        properties.update(custom_field_properties)
        properties = cls.add_relations_to_properties(properties, filter)
        return properties

    @classmethod
    def build_relation_serializers(cls, relation_names, filter) -> dict:
        return {name: cls.try_build_relation_serializer_instance(name, filter) for name in relation_names}

    @classmethod
    def try_build_relation_serializer_instance(cls, relation_name, filter):
        filter.step_into(relation_name)
        foreignkey_object = cls.get_related_object_by_property_name(relation_name)
        try:
            Serializer = foreignkey_object.build_serializer(filter)
        except Exception as e:
            logger.warning(f"could not create related serializer object with name: {relation_name}")
        else:
            return Serializer(many=cls.is_related_object_many(relation_name))
        finally:
            filter.step_out()

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
    def get_all_model_relations_names(cls, filter: SerializableModelFilter) -> list:
        names = cls.get_all_field_names_of_type(cls.relation_types)
        # TODO remove this _set when this has been handled
        names = filter.apply_relation_filter(names)
        return [name for name in names if ("_set" not in name)]

    @classmethod
    def get_all_attribute_names(cls, filter):
        names = cls.get_all_field_names_of_type(cls.attribute_types)
        return filter.apply_property_filter(names)

    @classmethod
    def get_all_field_names_of_type(cls, types) -> list:
        return [field.name for field in cls._meta.get_fields() if isinstance(field, types)]

    @classmethod
    def add_relations_to_properties(cls, properties, filter: SerializableModelFilter):
        relation_names = cls.get_all_model_relations_names(filter)
        properties[cls.META].fields += relation_names
        properties.update(cls.build_relation_serializers(relation_names, filter))
        return properties

    @classmethod
    def build_custom_field_properties(cls, filter):
        # custom filed properties is need for custom fields such as JSONField, that is not build in DRF
        custom_field_properties = {}
        for ModelField, SerializerField in cls.CUSTOM_FIELDS.items():
            names = cls.get_all_field_names_of_type(ModelField)
            names = filter.apply_property_filter(names)
            custom_field_properties.update({name: SerializerField() for name in names})
        return custom_field_properties
