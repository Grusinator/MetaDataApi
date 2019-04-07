import logging
from abc import ABCMeta, abstractmethod
from enum import Enum

from MetaDataApi.metadata.models import Object, ObjectRelation, Attribute, Schema, ObjectInstance, \
    ObjectRelationInstance, BaseAttributeInstance, FileAttributeInstance
from MetaDataApi.metadata.utils import DictUtils

logger = logging.getLogger(__name__)


class BaseRdfModel:
    __metaclass__ = ABCMeta

    schema_label = None

    class ObjectLabels(Enum):
        pass

    @classmethod
    @abstractmethod
    def _get_schema(cls) -> Schema:
        pass

    @classmethod
    @abstractmethod
    def _get_objects(cls):
        pass

    @classmethod
    @abstractmethod
    def _get_attributes(cls):
        pass

    @classmethod
    @abstractmethod
    def _get_object_relations(cls):
        pass

    class ObjectRelationLabels(Enum):
        pass

    class AttributeLabels(Enum):
        pass

    label_to_db_object = {
        ObjectLabels: Object,
        ObjectRelationLabels: ObjectRelation,
        AttributeLabels: Attribute
    }

    @classmethod
    def create_all_meta_objects(cls):
        cls._get_schema().save()
        [obj.save() for obj in cls._get_objects()]
        [att.save() for att in cls._get_attributes()]
        [obj_rel.save() for obj_rel in cls._get_object_relations()]

    @classmethod
    def is_schema_items_valid(cls):
        schema = [Schema.exists(cls._get_schema())]
        objs = [Object.exists_obj(obj) for obj in cls._get_objects()]
        atts = [Attribute.exists_att(att) for att in cls._get_attributes()]
        obj_rels = [ObjectRelation.exists_obj_rel(obj_rel) for obj_rel in cls._get_object_relations()]
        return all(schema + objs + atts + obj_rels)

    @classmethod
    def create_obj_inst(cls, obj: Object):
        obj_base = Object.exists_obj(obj)
        obj = ObjectInstance(base=obj_base)
        obj.save()
        return obj

    @classmethod
    def create_obj_rel_inst(cls, obj_rel: ObjectRelation, from_object: ObjectInstance, to_object: ObjectInstance):
        rel_base = ObjectRelation.exists_obj_rel(obj_rel)
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
        att_base = Attribute.exists_att(att)

        AttributeInstance = cls.get_attribute_instance_from_type(att_base.data_type)

        att_inst = AttributeInstance(
            object=parrent_obj_inst,
            base=att_base,
            value=value
        )
        if AttributeInstance is FileAttributeInstance:
            att_inst.value.save("steve.txt", value)

        att_inst.save()
        return att_inst


    @classmethod
    def get_attribute_instance_from_type(cls, type_as_string: str):
        datatype = DictUtils.inverse_dict(Attribute.data_type_map, type_as_string)
        return DictUtils.inverse_dict(BaseAttributeInstance.att_inst_to_type_map, datatype)
