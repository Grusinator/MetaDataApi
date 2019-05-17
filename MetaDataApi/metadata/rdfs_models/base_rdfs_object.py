import inspect
import logging

from MetaDataApi.metadata.models import ObjectInstance, Attribute, ObjectRelation, Object, Schema
from MetaDataApi.metadata.rdfs_models.descriptors.base_descriptor import BaseDescriptor
from MetaDataApi.metadata.rdfs_models.descriptors.relation_descriptor import ObjectRelationDescriptor
from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType

logger = logging.getLogger(__name__)


class BaseRdfsObject:
    SI = None
    schema_label = "meta_data_api"

    def __init__(self, inst_pk):
        self.object_instance = ObjectInstance.objects.get(pk=inst_pk)

    def set_attributes(self, json_obj: JsonType):
        self.update_from_json(json_obj)

    @property
    def base_object(self):
        return Object.exists_by_label(self.label, self.schema_label)

    @property
    def label(self):
        return type(self).__name__.lower()

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

    def initialize_schema(self):
        if not Schema.exists_by_label(self.schema_label):
            Schema.create_new_empty_schema(self.schema_label)
        if not Object.exists_by_label(self.label, self.schema_label):
            Object(schema=Schema.exists_by_label(self.schema_label), label=self.label).save()

        self.initialize_attributes()
        self.initialize_object_relations()

    def initialize_object_relations(self):
        relation_properties = self.get_all_schema_items_of_type(ObjectRelationDescriptor)
        for rel_property in relation_properties:
            ObjectRelation(
                label=rel_property.__name__,
                from_object=self.object_instance,
                to_object=rel_property.RdfsObjectType.object_instance,
                schema=Schema.exists_by_label(self.schema_label)
            ).create_if_not_exists()

    def initialize_attributes(self):
        attribute_properties = self.get_all_schema_items_of_type(ObjectRelationDescriptor)
        for att_property in attribute_properties:
            Attribute(
                label=att_property.__name__,
                object=self.object_instance,
                data_type=att_property.instance_type.data_type
            ).create_if_not_exists()

    @classmethod
    def get_all_schema_items_of_type(cls, descriptor_type: type) -> list:
        members = inspect.getmembers(cls, lambda m: isinstance(m, descriptor_type) or issubclass(m, descriptor_type))
        return [cls.as_descriptor(member) for member in members]

    @classmethod
    def as_descriptor(cls, member) -> BaseDescriptor:
        return member[1]
