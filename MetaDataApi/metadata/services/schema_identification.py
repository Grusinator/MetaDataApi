import json
from urllib import request
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from datetime import datetime
import dateutil


from inflection import underscore
from gensim.models import word2vec
from MetaDataApi.metadata.models import (
    Schema, Object,
    Attribute, ObjectRelation, UnmappedObject)

from MetaDataApi.datapoints.models import (
    ObjectInstance,
    StringAttributeInstance,
    ObjectRelationInstance)
from .base_functions import BaseMetaDataService

from .db_object_creation import DbObjectCreation


class SchemaIdentificationV2(DbObjectCreation):
    def __init__(self, *args, **kwargs):
        super(SchemaIdentificationV2, self).__init__()

        self.orms = [Object, Attribute]

        self.meta_data_list = []
        self.schema = None
        self.owner

        self._att_function = None
        self._object_function = None
        self._obj_rel_function = None

    #
    def identify_schema_from_data(self, input_data, schema_name,
                                  parrent_label=None):

        self.schema = self._try_get_item(Schema(label=schema_name))
        if not self.schema:
            self.schema = self.create_new_empty_schema(schema_name)

        try:
            person = self.get_foaf_person()
            self.touched_meta_items.append(person)
        except Exception as e:
            raise Exception("foaf person was not found")
        # TODO: Relate to logged in person object instead

        if parrent_label:
            input_data = {
                parrent_label: input_data
            }

        self.iterate_identify_schema_from_data(
            input_data, parrent_object=person)

        return self.touched_meta_items

    def iterate_identify_schema_from_data(self, input_data,
                                          parrent_object=None):
        if input_data is None:
            return

        if isinstance(input_data, list):
            # if its a list, there is no key, all we can do is to step
            # down but add all the data within to a new list
            # def func(x): return isinstance(x, (dict, list))

            # if any([func(x) for x in input_data]):
            #     pass

            for elm in input_data:
                # if isinstance(elm, (dict, list)):
                self.iterate_identify_schema_from_data(
                    elm, parrent_object)

            return

        # it must be some sort of value, this might only happen
        # if the parrent structure is a list, because if it is a dict
        # the value of the dict is tested for being an attribute
        elif not isinstance(input_data, dict):
            data_as_type = self.identify_datatype(input_data)
            datatype = type(data_as_type) # if data_as_type is not None else None
            # create the attribute with the parrent
            # label since its a list of values
            # we dont know what it is called

            if parrent_object is not None:
                att = Attribute(
                    label=parrent_object.label,
                    datatype=Attribute.data_type_map[datatype],
                    object=parrent_object
                )

                att = self._try_create_item(att)
            else:
                a = 1

            return

        for key, value in input_data.items():
            # this is likely a object if it contains other
            # attributes or objects
            if value is None:
                return

            # this must be an attribute
            # test if value dict only contains
            # "value", "unit" and whatever attr
            elif isinstance(value, (str, int, float)) or \
                    (isinstance(value, dict) and
                     self.dict_contains_only_attr(value)):
                    # it is probably an attribute

                data_as_type = self.identify_datatype(value)
                datatype = type(
                    data_as_type) #if data_as_type is not None else None

                att_obj = self._try_get_item(parrent_object)

                if att_obj.schema != self.schema:
                    raise Exception(
                        "dont create attributes connected to other schemas")
                if parrent_object is not None:
                    att = Attribute(
                        label=key,
                        datatype=Attribute.data_type_map[datatype],
                        object=att_obj)

                    att = self._try_create_item(att)

            # its probably a object
            else:
                obj = Object(
                    label=key,
                    schema=self.schema
                )

                # we need to add the object to the
                obj = self._try_create_item(
                    obj, parrent_label=parrent_object.label)

                if parrent_object:
                    obj_rel = ObjectRelation(
                        label="%s__to__%s" % (parrent_object.label, obj.label),
                        from_object=self._try_get_item(parrent_object),
                        to_object=self._try_get_item(obj),
                        schema=self.schema
                    )

                    obj_rel = self._try_create_item(obj_rel)

                # then iterate down the object value
                # to find connected objects
                self.iterate_identify_schema_from_data(
                    value, parrent_object=obj or parrent_object)

    #
    def create_instances_from_data(self, input_data, schema_name,
                                   parrent_label=None, owner=None):

        self.owner = owner
        self.schema = self._try_get_item(Schema(label=schema_name))
        if not self.schema:
            raise Exception("cant create data from native schema, "
                            "if schema does not exists. Try identify "
                            "schema from data first")

        # test if this is an url
        url_data = self.validate_url(input_data)

        # try to get the last dir of the url if applicable
        parrent_label = parrent_label or (
            url_data and "/".split(input_data)[-1])

        input_data = url_data or input_data
        # json data can either be list or dict
        if not isinstance(input_data, (dict, list)):
            input_data = json.loads(input_data)

        # create a base person to relate the data to
        try:
            person = ObjectInstance(
                base=self.get_foaf_person()
            )
            person.save()
        except Exception as e:
            raise Exception("foaf person was not found")
        # TODO: Relate to logged in foaf person object instance instead

        if parrent_label is not None:
            input_data = {parrent_label: input_data, }
            parrent_label = None

        objects, modified_data = self.iterate_create_instances_from_data(
            input_data, person, parrent_label=parrent_label)

        # only objects, remove attributes and relations
        unmapped_objects = list(filter(lambda x: isinstance(x, UnmappedObject),
                                       objects))

        # only objects, remove attributes and relations
        only_obj_objects = list(filter(lambda x: isinstance(x, ObjectInstance),
                                       objects))

        # relate to foaf
        # conn_objects, failed = self.connect_objects_to_foaf(only_obj_objects)

        # serialized_data = self.serialize_objects(objects)

        return modified_data, objects

    def iterate_create_instances_from_data(
            self, input_data, parrent_obj_inst, parrent_label=None):
        # for each branch in the tree check match for labels,
        # attribute labels and relations labels

        instance_list = []

        if isinstance(input_data, list):
            # if its a list, there is no key, all we can do is to step
            # down but add all the data within to a new list
            modified_data = []
            for elm in input_data:

                # if isinstance(elm, (dict, list)):
                objects, list_elm_data = \
                    self.iterate_create_instances_from_data(
                        elm, parrent_obj_inst)

                instance_list.extend(objects)
                modified_data.append(list_elm_data)

            # loop through and return data
            return instance_list, modified_data

        # it must be some sort of value, this might only happen
        # if the parrent structure is a list, because if it is a dict
        # the value of the dict is tested for being an attribute
        elif not isinstance(input_data, dict):
            modified_data = input_data

            # look for the parrent
            label = parrent_label or parrent_obj_inst.base.label

            att_inst, instance_list = self._identify_and_create_attribute(
                label, input_data, parrent_obj_inst, instance_list)

            if att_inst:
                # modify input data to include the attribute
                # return tuple with the att label that was found
                modified_data = (str(att_inst.base), input_data)
            else:
                instance_list.append(
                    UnmappedObject(
                        label=parrent_label,
                        parrent_label=label,
                        childrens=None
                    )
                )

            return instance_list, modified_data

        # cant copy values such as float
        modified_data = input_data.copy()

        for key, value in input_data.items():
            # this is likely a object if it contains other
            # attributes or objects

            # this must be an attribute
            # test if value dict only contains
            # "value", "unit" and whatever attr
            if isinstance(value, (str, int, float)) or \
                    (isinstance(value, dict) and
                     self.dict_contains_only_attr(value)):
                    # it is probably an attribute

                    # prepare the variables for the lookup
                if isinstance(value, dict):
                    att_value = value.get("value")
                else:
                    att_value = value

                # the key is the label we are looking for here
                att_inst, instance_list = self._identify_and_create_attribute(
                    key, att_value, parrent_obj_inst, instance_list)

                if att_inst:
                    # modify input data to include the attribute
                    self._add_object_label_to_dict_key(modified_data,
                                                       att_inst.base, key)
                else:
                    instance_list.append(
                        UnmappedObject(
                            label=key,
                            parrent_label=parrent_label or
                            parrent_obj_inst.base.label,
                            childrens=value
                        )
                    )
                    # attribute not found
                    # TODO: handle this better

            # its probably a object
            # assumption: it can only be a dict
            else:

                # check if the key is a label
                obj = self.find_label_in_metadata(
                    key, value, parrent=parrent_obj_inst)

                if isinstance(obj, Object):
                    # create object instance of the one found from label
                    obj_inst = ObjectInstance(base=obj)
                    obj_inst.save()
                    instance_list.append(obj_inst)

                    self._add_object_label_to_dict_key(modified_data,
                                                       obj, key)

                    # test if relation between parrent exists
                    obj_rel = self.relation_between_objects(
                        parrent_obj_inst, obj)

                    # if relation exist create instance
                    if obj_rel:
                        obj_rel_inst = ObjectRelationInstance(
                            from_object=parrent_obj_inst,
                            to_object=obj_inst,
                            base=obj_rel
                        )
                        obj_rel_inst.save()
                        instance_list.append(obj_rel_inst)

                    # TODO consider if it would be better if the object
                    # was not created in case the object relation does not
                    # exist

                    # update parrent object instance, since we are stepping
                    # down the branch after testing the relation
                    # parrent_obj_inst = obj_inst
                    # since we have parrent now, clar the parrent label
                    # it should only be set when we dont have a parrent
                    # ( no grand parrents count here)
                    # parrent_label = None

                # elif isinstance(obj, ObjectRelation):
                #     # dont act here, it should be created when
                #     # an object is identified

                #     # just step down
                #     pass
                else:

                    # nothing was found, the most recent key "label" should be
                    # used for further identification, especially for lists of
                    # values

                    instance_list.append(
                        UnmappedObject(
                            label=key,
                            parrent_label=parrent_label or
                            parrent_obj_inst.base.label,
                            childrens=list(value.keys())
                        )
                    )
                    parrent_label = key

                # then iterate down the object value
                # to find connected objects
                returned_objects, returned_data = \
                    self.iterate_create_instances_from_data(
                        value, obj_inst, parrent_label=None)
                instance_list.extend(returned_objects)

                # update the branch to the modified
                modified_data[key] = returned_data

        # when all objects are mapped return the instances
        return instance_list, modified_data

    def identify_schema_from_dataV2(self, input_data, schema_name,
                                  parrent_label=None):

        # setup how the loop handles each type of object occurrence
        self._att_function = self.try_create_attribute
        self._object_function = self.try_create_object
        self._obj_rel_function = self.try_create_object_relation

        self.schema = self._try_get_item(Schema(label=schema_name))
        if not self.schema:
            self.schema = self.create_new_empty_schema(schema_name)

        try:
            person = self.get_foaf_person()
            self.touched_meta_items.append(person)
        except Exception as e:
            raise Exception("foaf person was not found")
        # TODO: Relate to logged in person object instead

        if parrent_label:
            input_data = {
                parrent_label: input_data
            }

        self.iterate_data_generic(
            input_data, parrent_object=person)

        return self.touched_meta_items

    #
    def map_data_to_native_instances(self, input_data, schema_name,
                                     parrent_label=None, owner=None):

        # setup how the loop handles each type of object occurrence
        self.owner = owner
        self._att_function = self.try_create_attribute_instance
        self._object_function = self.try_create_object_instance
        self._obj_rel_function = self.try_create_object_relation_instance

        self.schema = self._try_get_item(Schema(label=schema_name))
        if not self.schema:
            raise Exception("cant create data from native schema, "
                            "if schema does not exists. Try identify "
                            "schema from data first")

        # test if this is an url
        url_data = self.validate_url(input_data)

        # try to get the last dir of the url if applicable
        parrent_label = parrent_label or (
            url_data and "/".split(input_data)[-1])

        input_data = url_data or input_data
        # json data can either be list or dict
        if not isinstance(input_data, (dict, list)):
            input_data = json.loads(input_data)

        # create a base person to relate the data to
        try:
            person = ObjectInstance(
                base=self.get_foaf_person()
            )
            person.save()
        except Exception as e:
            raise Exception("foaf person was not found")
        # TODO: Relate to logged in foaf person object instance instead

        if parrent_label is not None:
            input_data = {parrent_label: input_data, }

        self.iterate_data_generic(input_data, person)

        return None, self.added_instance_items

    def iterate_data_generic(self, input_data, parrent_object=None):
        if input_data is None:
            return

        if isinstance(input_data, list):
            # if its a list, there is no key, all we can do is to step
            # down but add all the data within to a new list
            # def func(x): return isinstance(x, (dict, list))

            # if any([func(x) for x in input_data]):
            #     pass

            for elm in input_data:
                # if isinstance(elm, (dict, list)):
                self.iterate_data_generic(
                    elm, parrent_object)
            return
        # it must be some sort of value, this might only happen
        # if the parrent structure is a list, because if it is a dict
        # the value of the dict is tested for being an attribute
        elif not isinstance(input_data, dict):
            if parrent_object is not None:
                self._att_function(parrent_object, input_data,
                                   None)
            return
        elif isinstance(input_data, dict):
            for key, value in input_data.items():
                # this is likely a object if it contains other
                # attributes or objects

                # this must be an attribute
                # test if value dict only contains
                # "value", "unit" and whatever attr
                if isinstance(value, self.att_types) or \
                        (isinstance(value, dict) and
                         self.dict_contains_only_attr(value)):
                        # it is probably an attribute

                    self._att_function(parrent_object, value, key)

                # its probably a object
                else:
                    obj = self._object_function(parrent_object, value, key)

                    obj_rel = self._obj_rel_function(parrent_object, obj, None)

                    # then iterate down the object value
                    # to find connected objects
                    self.iterate_data_generic(
                        value, parrent_object=obj or parrent_object)



    #
    def connect_objects_to_foaf(self, objects):
        foaf = self.get_foaf_person()
        objects_has_foaf = foaf in objects

        # objects_has_foaf = True

        extra_objects = []
        failed = []

        for obj in objects:
            # test if connected
            if objects_has_foaf and \
                    self.is_objects_connected(obj, foaf, objects):
                continue
            chain = self.find_shortest_path_to_foaf_person(obj)

            if chain:
                extra_objects.extend(chain)
            else:
                failed.append(obj)
        return extra_objects, failed

    def serialize_objects(self, object_list):
        # TODO: implement real serialization
        dummy_string = ', '.join(str(x) for x in object_list)

        return dummy_string

    def _validate_and_create_if_real_parrent(self, attribute_inst,
                                             assumed_parrent):
        # if the parrent object is not the "real" parrent
        # of the attribute, then create it
        if assumed_parrent is None or \
                attribute_inst.base.object != assumed_parrent.base:

            real_parrent = ObjectInstance(
                base=attribute_inst.base.object,
            )
            real_parrent.save()
        else:
            real_parrent = assumed_parrent

        attribute_inst.object = real_parrent

        return real_parrent

    def _identify_and_create_attribute(
            self, label, att_value,
            parrent_obj_inst, instance_list):

        data_as_type = self.identify_datatype(att_value)
        datatype = type(data_as_type) if data_as_type is not None else None
        # the key is the label
        att = self.find_label_in_metadata(
            label, datatype, look_only_for_items=[Attribute, ])

        if att and data_as_type is not None:
            # select which attribute instance type to use
            AttributeInstance = self.inverse_dict(
                self.att_inst_to_type_map, datatype)

            # default to string if None
            AttributeInstance = AttributeInstance or StringAttributeInstance
            att_inst = AttributeInstance(
                base=att,
                object=parrent_obj_inst,
                value=data_as_type
            )

            # real_parrent = self._validate_and_create_if_real_parrent(
            #     att_inst, parrent_obj_inst
            # )

            # make sure the connection is to the real parrent,
            # but this adobtion thing should not be done
            # TODO: handle this better, in native schemas it should
            # not be a problem

            att_inst.save()

            # if real_parrent != parrent_obj_inst:

            #     instance_list.append(real_parrent)

            instance_list.append(att_inst)

            return att_inst, instance_list

        else:

            # attribute not found
            return None, instance_list
        # TODO: handle this better

    def _add_object_label_to_dict_key(self, input_dict, item, key):
        conv = {
            Attribute: "A",
            Object: "O",
            ObjectRelation: "R"
        }

        # modify input data to include the attribute
        new_key = "%s -> %s:%s" % (
            key,
            conv.get(type(item)),
            item.label)
        # update the key
        input_dict[new_key] = input_dict.pop(key)
        return input_dict

    def relation_between_objects(self, from_obj, to_obj):
        def convert_to_base(obj):
            if isinstance(obj, ObjectInstance):
                return obj.base
            else:
                return obj

        from_obj = convert_to_base(from_obj)
        to_obj = convert_to_base(to_obj)

        try:
            return ObjectRelation.objects.get(
                from_object=from_obj,
                to_object=to_obj
            )
        except Exception as e:
            return None

    def validate_url(self, url):
        if not isinstance(url, str):
            return None
        val = URLValidator()
        try:
            val(url)
        except ValidationError as e:
            return None

        with request.urlopen(url) as resp:
            return resp.read().decode()

    def find_shortest_path_to_foaf_person(self, base_object):

        foaf_found, _ = self.iterate_find_related_obj(
            base_object, self.get_foaf_person(), discovered_objects=[])

        return foaf_found

    def iterate_find_related_obj(self, parrent_obj, find_obj,
                                 discovered_objects=[]):
        if isinstance(parrent_obj, (ObjectInstance,
                                    GenericAttributeInstance)):
            parrent_obj = parrent_obj.base
        # only relevant for first iteration, if the obj is an attribute
        if isinstance(parrent_obj, Attribute):
            parrent_obj = parrent_obj.object

        # dont look for allready searched objects
        connected_objects = filter(
            lambda x: x not in discovered_objects,
            parrent_obj.from_relations.all())

        # should maybe not be hardcoded
        for obj in connected_objects:
            if obj.label == find_obj.label and \
                    obj.schema.label == find_obj.schema.label:
                return [obj, ]

            obj_found, discovered_objects = self.iterate_find_related_obj(
                obj, discovered_objects)
            # if we have found something, just collapse and add the current
            # object
            if obj_found:
                obj_found.append(obj)
                return obj_found

            # discovered list as well

            discovered_objects.append(obj)

        # foaf person was not found, return what was discovered
        return None, discovered_objects

    def find_label_in_metadata(self, label, children=None, parrent=None,
                               look_only_for_items=None):
        # iterate through the vectorized  dataobjects,
        # mostly objects and attributes.
        # Add semantic vector to each object

        candidates = []
        # first, test if label exists in each object
        for orm in look_only_for_items or self.orms:
            objects = orm.objects.all()
            for obj in objects:
                score = self.likelihood_score(label, obj)
                if score > 0.7:
                    candidates.append((obj, score))
        # get candidate with the max score
        if len(candidates) == 0:
            return None
        else:
            return max(candidates, key=lambda x: x[1])[0]

    def likelihood_score(self, label, obj, data_type=None):
        v1 = self.compare_labels(label, obj.label)

        # datatype is only used in case of attributes
        if isinstance(obj, Attribute) and data_type:
            v2 = self.datatype_match(obj, data_type)
        # if it is an object we can look at the relations
        # and see if it matches related objects or attributes
        elif isinstance(obj, Object) and None:
            v2 = self.relations_match()
        else:
            v2 = 0
        return v1 + v2

    def compare_labels(self, label1, label2):
        label1 = underscore(label1)
        label2 = underscore(label2)

        # this is a perfect match
        if label1 == label2:
            return 1
        else:
            # probably need more preprocessing
            # return self.model.similarity(label1, label2)
            return 0

    def datatype_match(self, object, data_type):
        return 0

    def relations_match(self, object, json_desendents, json_parrent):
        """
        check if there are similarities with the structure
        """
        return 0
