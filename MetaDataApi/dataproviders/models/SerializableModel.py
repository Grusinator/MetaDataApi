import logging

from django.db.models import TextField, IntegerField, FloatField, BooleanField, ForeignKey, OneToOneField, ManyToOneRel, \
    OneToOneRel
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor, ReverseManyToOneDescriptor
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

    def serialize(self, filter=SerializableModelFilter()):
        if not filter.current_object_name:
            # TODO ._meta.model_name is not be the correct property. fix.
            logger.debug(f"using default model name as starting name: {self._meta.model_name}")
            filter.current_object_name = self._meta.model_name
        Serializer = type(self).build_serializer(filter)
        data = Serializer(self).data
        return JsonUtils.dump_and_load(data)

    @classmethod
    def deserialize(cls, data: JsonType, filter=SerializableModelFilter()):
        deserialized_object = cls.deserialize_to_objects(data, filter)
        return deserialized_object

    @classmethod
    def deserialize_to_objects(cls, data, filter: SerializableModelFilter):
        Serializer = cls.build_serializer(filter)
        serializer = Serializer(data=data)
        if not serializer.is_valid():
            raise Exception(f"could not deserialize, due to error: {serializer.errors}")
        serialized_object = serializer.save()
        return serialized_object

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

        properties = cls.add_create_method_to_properties(properties)
        return properties

    @classmethod
    def build_relation_serializers(cls, relation_names, filter) -> dict:
        return {name: cls.try_build_relation_serializer_instance(name, filter) for name in relation_names}

    @classmethod
    def try_build_relation_serializer_instance(cls, relation_name, filter):
        filter.step_into(relation_name)
        related_object = cls.get_related_object_by_property_name(relation_name)
        try:
            Serializer = related_object.build_serializer(filter)
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
        names = filter.apply_relation_filter(names)
        return names

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

    @classmethod
    def create(cls, validated_data):
        properties = cls.get_properties_from_data(validated_data)
        base_instance = cls.objects.create(**properties)
        cls.create_related_object(base_instance, validated_data)
        return base_instance

    @classmethod
    def create_related_object(cls, base_instance, validated_data):
        relations = cls.get_relations_from_data(validated_data)
        for relation_name, relation_data in relations.items():
            relation_object = cls.get_relation_object(relation_name)
            parrent_data = cls.create_parrent_data(base_instance, relation_name)
            if not cls.is_related_object_many(relation_name):
                relation_data = [relation_data]
            for relation_data_element in relation_data:
                relation_object.objects.create(**relation_data_element, **parrent_data)

    @classmethod
    def create_parrent_data(cls, base_instance, relation_name):
        to_parrent_related_name = cls.get_related_name(relation_name)
        parrent_info = {to_parrent_related_name: base_instance}
        return parrent_info

    @classmethod
    def add_create_method_to_properties(cls, properties):
        properties["create"] = cls.create
        return properties

    @classmethod
    def get_properties_from_data(cls, data):
        names = cls.get_all_field_names_of_type(cls.attribute_types)
        return {name: val for name, val in data.items() if name in names}

    @classmethod
    def get_relations_from_data(cls, data) -> dict:
        names = cls.get_all_field_names_of_type(cls.relation_types)
        return {name: val for name, val in data.items() if name in names}

    @classmethod
    def get_relation_object(cls, relation_name):
        return cls.get_related_field(relation_name).model

    @classmethod
    def get_related_name(cls, relation_name):
        return cls.get_related_field(relation_name).name

    @classmethod
    def get_related_field(cls, relation_name):
        related_object = getattr(cls, relation_name)
        # if isinstance(related_object, (OneToOneRel, ManyToOneRel)):
        #     return related_object.related.field
        # elif isinstance(related_object, (OneToOneField, ForeignKey)):
        #     return related_object.field
        if isinstance(related_object, (ReverseOneToOneDescriptor,)):
            return related_object.related.field
        elif isinstance(related_object, (ReverseManyToOneDescriptor,)):
            return related_object.field
        else:
            raise AttributeError(f"unknown relation type: {type(related_object)}")
