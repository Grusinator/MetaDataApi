
from MetaDataApi.metadata.services.base_functions import BaseMetaDataService

from MetaDataApi.metadata.models import *
from MetaDataApi.datapoints.models import *


class DbObjectCreation(BaseMetaDataService):

    def __init__(self, *args, **kwargs):
        self.owner = None
        self.schema = None
        super(DbObjectCreation, self).__init__()

    def try_create_attribute(self, parrent_object, data, label):
        data_as_type = self.identify_datatype(input_data)
        datatype = type(data_as_type) if data_as_type is not None else None

        if parrent_object is not None:
            label = label or parrent_object.label

            att = Attribute(
                label=label,
                datatype=Attribute.data_type_map[datatype],
                object=self._try_get_item(parrent_object)
            )

            return self._try_create_item(att)
        else:
            a = 1

    def try_create_object(self, parrent_object, data, label):

        obj = Object(
            label=label,
            schema=self.schema
        )

        # we need to add the object to the
        return self._try_create_item(
            obj,
            parrent_label=parrent_object.label)

    def try_create_object_relation(self, parrent_object, data, label):

        if parrent_object is not None:
            label = label or "%s__to__%s" % (parrent_object.label, obj.label)

            obj_rel = ObjectRelation(
                label=label,
                from_object=self._try_get_item(parrent_object),
                to_object=self._try_get_item(data),
                schema=self.schema
            )

            return self._try_create_item(obj_rel)
        else:
            a = 1

    def try_create_attribute_instance(self, parrent_object, data, label):
        data_as_type = self.identify_datatype(data)
        datatype = type(data_as_type) if data_as_type is not None else None
        # create the attribute with the parrent
        # label since its a list of values
        # we dont know what it is called

        if parrent_object is not None:
            label = label or parrent_object.base.label

            att = Attribute(
                label=label,
                datatype=Attribute.data_type_map[datatype],
                object=self._try_get_item(parrent_object.base)
            )

            att = self._try_get_item(att)

            # Create the instance
            if att is not None:
                AttributeInstance = self.att_to_att_inst(att)
                att_inst = AttributeInstance(
                    base=att,
                    value=data_as_type,
                    object=parrent_object
                )
                att_inst.save()
                return att_inst

    def try_create_object_instance(self, parrent_object, data, label):
        obj = Object(
            label=label,
            schema=self.schema
        )

        # we need to add the object to the
        obj = self._try_get_item(
            obj, parrent_label=parrent_object.base.label)

        if obj:
            obj_inst = ObjectInstance(
                base=obj,
                owner=self.owner
            )
            obj_inst.save()

            return obj_inst

    def try_create_object_relation_instance(self, parrent_object, data, label):
        # data is the to_object, its just for consistency
        # its called data

        if parrent_object is not None and data is not None:
            label = label or "%s__to__%s" % (
                parrent_object.base.label, data.base.label)

            obj_rel = ObjectRelation(
                label=label,
                from_object=self._try_get_item(parrent_object.base),
                to_object=self._try_get_item(data.base),
                schema=self.schema
            )
            obj_rel = self._try_get_item(obj_rel)

            if obj_rel is not None:
                obj_rel_inst = ObjectRelationInstance(
                    base=obj_rel,
                    from_object=parrent_object,
                    to_object=data
                )
                obj_rel_inst.save()

                return obj_rel_inst
