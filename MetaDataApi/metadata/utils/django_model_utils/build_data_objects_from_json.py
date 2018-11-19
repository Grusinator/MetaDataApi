
from MetaDataApi.metadata.models import (
    # meta
    Object, Attribute, ObjectRelation, Schema,
    # instances
    RawData,
    ObjectInstance,
    ObjectRelationInstance,
    FloatAttributeInstance,
    StringAttributeInstance,
    IntAttributeInstance,
    BoolAttributeInstance,
    ImageAttributeInstance)


from ..json_utils.json_iterator import IJsonIterator
from MetaDataApi.metadata.utils.common_utils.data_type_utils import DataTypeUtils

#from MetaDataApi.metadata.models.meta import Schema


class BuildDataObjectsFromJson(IJsonIterator):
    from_obj_search_str = "from_relations__from_object__"
    to_obj_search_str = "to_relations__to_object__"

    def __init__(self, schema, owner):
        self.schema = schema
        self.owner = owner
        self.added_instance_items = []

        super(BuildDataObjectsFromJson, self).__init__()

    def handle_attributes(self, parrent_object, data, label):
        att = Attribute.exists(label, parrent_object.label)

        # identify datatype
        data_as_type = DataTypeUtils.identify_data_type(data)
        data_type = type(data_as_type)

        # it does not exists
        if att is None and parrent_object is not None:

            att = Attribute(
                label=label,
                data_type=Attribute.data_type_map[data_type],
                object=parrent_object
            )

            att.save()

        #
        att_inst = AttributeInstance.exists()

        if att_inst is not None:
            return att_inst
        else:
            # Create the instance
            AttributeInstance = self.att_to_att_inst(att)
            att_inst = AttributeInstance(
                base=att,
                value=data_as_type,
                object=parrent_object,
                owner=self.owner
            )
            try:
                att_inst.save()
                self.added_instance_items.append(att_inst)
                return att_inst
            except Exception as e:
                logger.error("object_create_" + str(e))

    def handle_objects(self, parrent_object, data, label):
        obj = Object.exists(label, self.schema.label)

        # it does not exists
        if obj is None:
            obj = Object(
                label=label,
                schema=self.schema
            )

        obj_inst = ObjectInstance.exists(label, data)

        if obj_inst is not None:
            return obj_inst
        else:
            # Create instance
            obj_inst = ObjectInstance(
                base=obj,
                owner=self.owner
            )
            try:
                obj_inst.save()
                self.added_instance_items.append(obj_inst)
                return obj_inst
            except Exception as e:
                logger.error("object_create_" + str(e))

    def handle_object_relations(self, parrent_object, to_object, label):
        obj_rel = ObjectRelation.exists(label, parrent_object, to_object)

        if obj_rel is None:
            label = label or "%s__to__%s" % (
                parrent_object.label, to_object.label)

            obj_rel = ObjectRelation(
                label=label,
                from_object=self._try_get_item(parrent_object),
                to_object=self._try_get_item(to_object),
                schema=self.schema
            )
            obj_rel.save()

        obj_rel_inst = ObjectRelationInstance.exists()

        if obj_rel_inst is not None:
            return obj_rel_inst
        else:
            obj_rel_inst = ObjectRelationInstance(
                base=obj_rel,
                from_object=parrent_object,
                to_object=to_object,
                owner=self.owner
            )
            try:
                obj_rel_inst.save()
                self.added_instance_items.append(obj_rel_inst)
                return obj_rel_inst
            except Exception as e:
                logger.error("object_create_" + str(e))

    def build_from_json(self, data, parrent_object=None):
        self.iterate_json_tree(data, parrent_object)
        return self.added_instance_items
