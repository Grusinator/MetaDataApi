import inspect
import logging

from MetaDataApi.metadata.models import ObjectInstance, Attribute, ObjectRelation, Object, Schema
from MetaDataApi.metadata.rdfs_models.descriptors.attributes.base_attribute_descriptor import BaseAttributeDescriptor
from MetaDataApi.metadata.rdfs_models.descriptors.base_descriptor import BaseDescriptor
from MetaDataApi.metadata.rdfs_models.descriptors.relation_descriptor import ObjectRelationDescriptor
from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType

logger = logging.getLogger(__name__)


class BaseRdfsObject:
    schema_label = "meta_data_api"

    def __init__(self, inst_pk):
        self.object_instance = ObjectInstance.objects.get(pk=inst_pk)

    def set_attributes(self, json_obj: JsonType):
        self.update_from_json(json_obj)

    @property
    def base_object(self):
        return Object.exists_by_label(self.object_label(), self.schema_label)

    @classmethod
    def object_label(cls):
        return cls.__name__.lower()

    @classmethod
    def get_object(cls):
        return Object.exists_by_label(cls.object_label(), cls.schema_label)

    def create_self(self, json_object: dict):
        self.object_instance = ObjectInstance(base=self.base_object)
        self.object_instance.save()
        self.update_from_json(json_object)

    def update_from_json(self, json_object):
        if json_object is not None:
            for key, value in json_object.items():
                try:
                    setattr(self, key, value)
                except Exception as e:
                    logger.warning("could not set key: %s  with value: %s ____ exc: %s" % (key, value, e))
                    pass

    @classmethod
    def initialize_schema_objects(cls):
        cls.initialize_schema()
        cls.initialize_object()
        cls.initialize_attributes()
        cls.initialize_object_relations()

    @classmethod
    def initialize_object(cls):
        if not cls.get_object():
            Object(
                schema=Schema.exists_by_label(cls.schema_label),
                label=cls.object_label()
            ).save()

    @classmethod
    def initialize_schema(cls):
        if not Schema.exists_by_label(cls.schema_label):
            Schema.create_new_empty_schema(cls.schema_label)

    @classmethod
    def initialize_object_relations(cls):
        relation_properties = cls.get_all_schema_items_of_type(ObjectRelationDescriptor)
        for rel_property in relation_properties:
            ObjectRelation(
                label=rel_property.__name__,
                from_object=cls.get_object(),
                to_object=rel_property.RdfsObjectType.object_instance,
                schema=Schema.exists_by_label(cls.schema_label)
            ).create_if_not_exists()

    @classmethod
    def initialize_attributes(cls):
        attribute_properties = cls.get_all_schema_items_of_type(BaseAttributeDescriptor)
        for att_property in attribute_properties:
            Attribute(
                label=att_property.__name__,
                object=cls.get_object(),
                data_type=att_property.instance_type.data_type
            ).create_if_not_exists()

    @classmethod
    def get_all_schema_items_of_type(cls, descriptor_type: type) -> list:
        members = inspect.getmembers(cls, lambda m: cls.is_instance_or_subclass(m, descriptor_type))
        return [cls.as_descriptor(member) for member in members]

    @staticmethod
    def is_instance_or_subclass(m, descriptor_type):
        return isinstance(m, descriptor_type) or inspect.isclass(m) and issubclass(m, descriptor_type)

    @classmethod
    def as_descriptor(cls, member) -> BaseDescriptor:
        return member[1]
