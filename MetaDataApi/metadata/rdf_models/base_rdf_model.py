import logging
from abc import ABCMeta
from enum import Enum

from django.core.exceptions import ObjectDoesNotExist

from MetaDataApi.metadata.models import Object, ObjectRelation, Attribute, Schema, ObjectInstance, \
    ObjectRelationInstance, BaseAttributeInstance, FileAttributeInstance
from MetaDataApi.metadata.utils import DictUtils

logger = logging.getLogger(__name__)


class BaseRdfModel:
    __metaclass__ = ABCMeta

    schema_label = None

    class ObjectLabels(Enum):
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
    def validate(cls):
        cls.validate_schema()
        cls.validate_enums()

    @classmethod
    def validate_enums(cls):

        for labels, db_object in cls.label_to_db_object.items():
            for label in labels:
                cls.try_get_db_object(db_object, label)

    @classmethod
    def try_get_db_object(cls, db_object, label):
        try:
            db_object.objects.get(label=label)
        except ObjectDoesNotExist as e:
            logger.error(str(e) + "| label not found: " + str(label))

    @classmethod
    def validate_schema(cls):
        Schema.objects.get(label=cls.schema_label)

    @classmethod
    def create_obj_inst(cls, label: ObjectRelationLabels):
        obj_base = Object.objects.get(label=label.value, schema=cls.get_schema())
        obj = ObjectInstance(base=obj_base)
        obj.save()
        return obj

    @classmethod
    def create_obj_rel_inst(cls, rel_label: ObjectRelationLabels, from_object, to_object):
        rel_base = ObjectRelation.objects.get(label=rel_label.value, schema=cls.get_schema())
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
                                    attribute_label: AttributeLabels,
                                    value):
        att_base = Attribute.objects.get(
            label=attribute_label.value,
            object=parrent_obj_inst.base
        )

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
    def get_schema(cls):
        return Schema.objects.get(label=cls.schema_label)

    @classmethod
    def get_attribute_instance_from_type(cls, type_as_string: str):
        datatype = DictUtils.inverse_dict(Attribute.data_type_map, type_as_string)
        return DictUtils.inverse_dict(BaseAttributeInstance.att_inst_to_type_map, datatype)
