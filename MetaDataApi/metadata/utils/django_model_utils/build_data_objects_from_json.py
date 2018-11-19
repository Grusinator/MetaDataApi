
from MetaDataApi.metadata.models.meta import (
    Object, Attribute, ObjectRelation, Schema,
)
from MetaDataApi.metadata.models.instances import (
    ObjectInstance,
    ObjectRelationInstance,
    BaseAttributeInstance,
    # FloatAttributeInstance,
    # StringAttributeInstance,
    # IntAttributeInstance,
    # BoolAttributeInstance,
    # ImageAttributeInstance
)


from ..json_utils.json_iterator import IJsonIterator
from MetaDataApi.metadata.utils.common_utils.data_type_utils import DataTypeUtils
from MetaDataApi.metadata.utils.common_utils import DictUtils
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils

import logging
logger = logging.getLogger(__name__)

# from MetaDataApi.metadata.models.meta import Schema


class BuildDataObjectsFromJson(IJsonIterator):

    def __init__(self, schema, owner):
        self.schema = schema
        self.owner = owner
        self.added_instance_items = []

        super(BuildDataObjectsFromJson, self).__init__()

    def save_obj(self, obj):
        try:
            obj.save()
            if not hasattr(obj, "label"):
                self.added_instance_items.append(obj)
            return obj

        except Exception as e:
            label = obj.label if hasattr(obj, "label") else obj.base.label
            logger.error(
                """Could not create obj: %s of type: %s, caused by the following
                 error: %s""" % (type(obj), label, str(e))
            )
            del obj

    def handle_attributes(self, parrent_object: ObjectInstance,
                          data, label: str):
        if parrent_object is None:
            return None

        # TODO handle list structures better fix for when list with values
        label = label or parrent_object.base.label

        att = Attribute.exists(label, parrent_object.base.label)

        # identify datatype
        data_as_type = DataTypeUtils.identify_data_type(data)
        data_type = type(data_as_type)

        # it does not exists
        if att is None:

            att = Attribute(
                label=label,
                data_type=Attribute.data_type_map[data_type],
                object=parrent_object.base
            )
            return self.save_obj(att)

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
            self.save_obj(obj)

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

        obj_rel = ObjectRelation.exists(
            label, parrent_object.base.label, to_object.base.label)

        if obj_rel is None:
            label = label or "%s__to__%s" % (
                parrent_object.base.label, to_object.base.label)

            obj_rel = ObjectRelation(
                label=label,
                from_object=parrent_object.base,
                to_object=to_object.base,
                schema=self.schema
            )
            self.save_obj(obj_rel)

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
