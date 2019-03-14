import logging

from django.db import IntegrityError, transaction

from metadata.models import (
    ObjectInstance,
    ObjectRelationInstance,
    BaseAttributeInstance,
    # FloatAttributeInstance,
    # StringAttributeInstance,
    # IntAttributeInstance,
    # BoolAttributeInstance,
    # ImageAttributeInstance
)
from metadata.models.meta import (
    Object, Attribute, ObjectRelation, )
from metadata.utils.common_utils import DictUtils
from metadata.utils.common_utils.data_type_utils import DataTypeUtils
from metadata.utils.json_utils.json_iterator import IJsonIterator

logger = logging.getLogger(__name__)


# from metadata.models.meta import Schema


def convert_dict_attribute_type(data):
    data.get("value")


class BuildDataObjectsFromJson(IJsonIterator):

    def __init__(self, schema, owner):
        self.schema = schema
        self.owner = owner
        self.added_instance_items = []

        super(BuildDataObjectsFromJson, self).__init__()

    def save_obj(self, obj):
        try:
            with transaction.atomic():
                obj.save()

            if not hasattr(obj, "label"):
                self.added_instance_items.append(obj)
            return obj

        except (IntegrityError, Exception) as e:
            label = obj.label if hasattr(obj, "label") else obj.base.label
            logger.error(
                """Could not create obj: %s of type: %s, caused by the following
                 error: %s""" % (type(obj).__name__, label, str(e))
            )
            # could not be created, so delete
            # obj.delete()
            del obj

    def handle_attributes(self, parrent_object: ObjectInstance,
                          data, label: str):
        if parrent_object is None:
            return None

        # TODO handle list structures better fix for when list with values
        label = label or parrent_object.base.label

        att = Attribute.exists(label, parrent_object.base.label)

        # TODO handle if the data of an attribute is a dict
        if isinstance(data, dict):
            unit = data.get('unit')
            data = data.get('value')

        # identify datatype
        data_as_type = DataTypeUtils.identify_data_type(data)
        data_type = type(data_as_type)

        if att is None:
            att = Attribute(
                label=label,
                data_type=Attribute.data_type_map[data_type],
                object=parrent_object.base
            )
            if not self.save_obj(att):
                return None

        # get the corresponding attribute type class
        AttributeInstance = DictUtils.inverse_dict(
            BaseAttributeInstance.att_inst_to_type_map,
            data_type
        )

        # check if an attribute of such type exists
        att_inst = AttributeInstance.exists(
            label, parrent_object.pk, data_as_type)

        if att_inst is not None:
            return att_inst
        else:
            # Create the instance
            att_inst = AttributeInstance(
                base=att,
                value=data_as_type,
                object=parrent_object,
                owner=self.owner
            )

            return self.save_obj(att_inst)

    def handle_objects(self, parrent_object: ObjectInstance, data, label: str):
        obj = Object.exists(label, self.schema.label)

        # it does not exists
        if obj is None:
            obj = Object(
                label=label,
                schema=self.schema
            )
            if not self.save_obj(obj):
                return None

        obj_inst = ObjectInstance.exists(label, data)

        if obj_inst is not None:
            return obj_inst
        else:
            # Create instance
            obj_inst = ObjectInstance(
                base=obj,
                owner=self.owner
            )
            return self.save_obj(obj_inst)

    def handle_object_relations(self, parrent_object: ObjectInstance,
                                to_object: ObjectInstance, label: str):
        if parrent_object is None or to_object is None:
            return None

        # when loading json the relations is just binded together by:
        #  [label]__to__[label]
        label = label or "%s__to__%s" % (
            parrent_object.base.label, to_object.base.label)

        obj_rel = ObjectRelation.exists(
            label, parrent_object.base.label,
            to_object.base.label, self.schema.label)

        if obj_rel is None:
            obj_rel = ObjectRelation(
                label=label,
                from_object=parrent_object.base,
                to_object=to_object.base,
                schema=self.schema
            )
            if not self.save_obj(obj_rel):
                return None

        obj_rel_inst = ObjectRelationInstance.exists(
            label, obj_rel.from_object, obj_rel.to_object)

        if obj_rel_inst is not None:
            return obj_rel_inst
        else:
            obj_rel_inst = ObjectRelationInstance(
                base=obj_rel,
                from_object=parrent_object,
                to_object=to_object,
                owner=self.owner
            )

        self.save_obj(obj_rel_inst)

        return obj_rel_inst

    def build_from_json(self, data, parrent_object=None):
        self.iterate_json_tree(data, parrent_object)
        return self.added_instance_items
