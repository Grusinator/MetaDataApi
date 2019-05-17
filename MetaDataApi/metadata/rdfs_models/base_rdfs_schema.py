import inspect
import logging
from abc import ABCMeta
from enum import Enum

from MetaDataApi.metadata.models import Object, ObjectRelation, Attribute, Schema, ObjectInstance, \
    ObjectRelationInstance, BaseAttributeInstance, FileAttributeInstance

logger = logging.getLogger(__name__)


class BaseRdfsSchema:
    __metaclass__ = ABCMeta

    schema_label = None

    class SchemaItems:
        pass

    class ObjectLabels(Enum):
        pass

    @classmethod
    def _get_schema(cls) -> Schema:
        return cls.get_all_schema_items_of_type(Schema)[0]

    @classmethod
    def _get_objects(cls) -> list:
        return cls.get_all_schema_items_of_type(Object)

    @classmethod
    def _get_attributes(cls):
        return cls.get_all_schema_items_of_type(Attribute)

    @classmethod
    def _get_object_relations(cls):
        return cls.get_all_schema_items_of_type(ObjectRelation)

    @classmethod
    def get_all_schema_items_of_type(cls, meta_type: type):
        members = inspect.getmembers(cls.SchemaItems, lambda m: isinstance(m, meta_type))
        return [member[1] for member in members]

    @classmethod
    def create_all_meta_objects(cls):
        schema = cls._get_schema().create_if_not_exists()

        objects = [cls.save_object(obj, schema) for obj in cls._get_objects()]
        attrs = [cls.save_attribute(att, objects) for att in cls._get_attributes()]
        obj_rels = [cls.save_object_rel(obj_rel, objects, schema) for obj_rel in cls._get_object_relations()]
        return objects + attrs + obj_rels

    @classmethod
    def save_object(cls, obj, schema):
        obj.schema = schema
        return obj.create_if_not_exists()

    @classmethod
    def save_attribute(cls, att, objects: list):
        obj_label = att.object.label
        # we have to update the object to a newly fetched or saved because otherwise the pk is not in the object
        att.object = list(filter(lambda o: o.label == obj_label, objects))[0]
        return att.create_if_not_exists()

    @classmethod
    def save_object_rel(cls, obj_rel, objects: list, schema: Schema):
        from_obj_label = obj_rel.from_object.label
        to_obj_label = obj_rel.to_object.label
        # we have to update the object to a newly fetched or saved because otherwise the pk is not in the object
        obj_rel.from_object = list(filter(lambda o: o.label == from_obj_label, objects))[0]
        obj_rel.to_object = list(filter(lambda o: o.label == to_obj_label, objects))[0]
        obj_rel.schema = schema
        return obj_rel.create_if_not_exists()

    @classmethod
    def do_schema_items_exists(cls):
        schema = [Schema.exists(cls._get_schema())]
        objs = [Object.exists(obj) for obj in cls._get_objects()]
        atts = [Attribute.exists(att) for att in cls._get_attributes()]
        obj_rels = [ObjectRelation.exists(obj_rel) for obj_rel in cls._get_object_relations()]
        return all(schema + objs + atts + obj_rels)

    @classmethod
    def create_obj_inst(cls, obj: Object):
        obj_base = Object.exists(obj)
        obj = ObjectInstance(base=obj_base)
        obj.save()
        return obj

    @classmethod
    def create_obj_rel_inst(cls, obj_rel: ObjectRelation, from_object: ObjectInstance, to_object: ObjectInstance):
        rel_base = ObjectRelation.exists(obj_rel)
        rel = ObjectRelationInstance(
            base=rel_base,
            from_object=from_object,
            to_object=to_object
        )
        rel.save()
        return rel

    @classmethod
    def create_att_inst_to_obj_inst(cls,
                                    parrent_obj_inst: ObjectInstance,
                                    att: Attribute,
                                    value):
        att_base = Attribute.exists(att)

        SpecificAttributeInstance = BaseAttributeInstance.get_attribute_instance_from_data_type(att_base.data_type)

        att_inst = SpecificAttributeInstance(
            object=parrent_obj_inst,
            base=att_base,
            value=value
        )
        if SpecificAttributeInstance is FileAttributeInstance:
            att_inst.value.save(value.name, value)

        att_inst.save()
        return att_inst

    @classmethod
    def update_att_of_obj(cls, att_inst: BaseAttributeInstance, value):
        att_inst.value = value
        att_inst.save()
