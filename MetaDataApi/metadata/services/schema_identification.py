import json
from urllib import request
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from datetime import datetime
from dateutil import parser


from inflection import underscore
from gensim.models import word2vec
from MetaDataApi.metadata.models import (
    Schema, Object,
    Attribute, ObjectRelation)

from MetaDataApi.datapoints.models import (
    ObjectInstance,
    GenericAttributeInstance,
    ObjectRelationInstance)
from .base_functions import BaseMetaDataService


class SchemaIdentification(BaseMetaDataService):
    def __init__(self, *args, **kwargs):
        super(SchemaIdentification, self).__init__()
        # consider using sports articles for corpus
        # sentences = word2vec.Text8Corpus('text8')

        self.orms = [Object, Attribute]

        # self.model = word2vec.Word2Vec(sentences, size=200)

    def identify_data(self, input_data):
        """ this is the main function that handles all the
        restructuring of the data.
        """
        # test if this is an url
        input_data = self.validate_url(input_data) or input_data

        input_data = json.loads(input_data)

        # create a base person to relate the data to
        try:
            person = ObjectInstance(
                base=self._try_get_item(Object, label="person")
            )
        except:
            raise Exception("foaf person was not found")
        # TODO: Relate to logged in person object instead

        objects, modified_data = self.iterate_data(input_data, person)

        # only objects, remove attributes and relations
        ony_obj_objects = filter(lambda x: isinstance(x, ObjectInstance),
                                 objects)

        # relate to foaf
        objects, failed = self.connect_objects_to_foaf(ony_obj_objects)

        serialized_data = self.serialize_objects(objects)

        return modified_data

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

    def iterate_data(self, input_data, parrent_obj_inst):
        # for each branch in the tree check match for labels,
        # attribute labels and relations labels

        modified_data = input_data.copy()

        instance_list = []

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
                    att_value = str(value)

                data_type = self.identify_datatype(att_value)

                # the key is the label
                att = self.find_label_in_metadata(
                    key, data_type, look_only_for_items=[Attribute, ])

                if att:
                    # if the parrent object is not the "real" parrent
                    # of the attribute, then create it
                    if att.object != parrent_obj_inst.base:
                        real_parrent = ObjectInstance(
                            base=att.object,
                        )
                        instance_list.append(real_parrent)
                    else:
                        real_parrent = parrent_obj_inst

                    instance_list.append(
                        GenericAttributeInstance(
                            base=att,
                            object=real_parrent,
                            value=att_value
                        )
                    )

                    # modify input data to include the attribute
                    self.add_object_label_to_dict(modified_data,
                                                  att, key)

                else:
                    # attribute not found
                    pass
                # TODO: handle this better

            # its probably a object
            else:
                # check if the key is a label
                obj = self.find_label_in_metadata(
                    key, value)

                if isinstance(obj, Object):
                    # create object instance of the one found from label
                    obj_inst = instance_list.append(
                        ObjectInstance(
                            base=obj
                        )
                    )

                    self.add_object_label_to_dict(modified_data,
                                                  obj, key)

                    # test if relation between parrent exists
                    obj_rel = self.relation_between_objects(
                        parrent_obj_inst, obj)

                    # if relation exist create instance
                    if obj_rel:
                        parrent_obj_inst = ObjectRelationInstance(
                            from_obj=parrent_obj_inst,
                            to_obj=obj_inst,
                        )
                        instance_list.append(parrent_obj_inst)

                        self.add_object_label_to_dict(modified_data,
                                                      obj_rel, key)

                elif isinstance(obj, ObjectRelation):
                    # dont act here, it should be created when
                    # an object is identified

                    # just step down
                    pass

                # then iterate down the object value
                # to find connected objects
                returned_objects, returned_data = self.iterate_data(
                    value, parrent_obj_inst)
                instance_list.extend(returned_objects)

                # update the branch to the modified
                modified_data[key] = returned_data

        # when all objects are mapped return the instances
        return instance_list, modified_data

    def add_object_label_to_dict(self, input_dict, item, key):
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

    def relation_between_objects(from_obj, to_obj):
        def convert_to_base(obj):
            if isinstance(obj, ObjectInstance):
                return obj.base
            else:
                return obj

        from_obj = convert_to_base(from_obj)
        to_obj = convert_to_base(to_obj)

        try:
            return ObjectRelation.objects.get(
                from_obj=from_obj,
                to_obj=to_obj
            )
        except:
            return None

    def dict_contains_only_attr(self, data):
        # if its not a dict, then its not an
        # attribute
        if not isinstance(data, dict):
            return False

        data = data.copy()
        if len(data) == 0:
            return False
        attr_names = ["value", "unit"]
        attrs = [data.pop(name, None) for name in attr_names]

        return len(data) == 0

    def validate_url(self, url):
        val = URLValidator()
        try:
            val(url)
        except ValidationError as e:
            return None

        with request.urlopen(url) as resp:
            return resp.read().decode()

    def identify_datatype(self, element):
        # even though it is a string,
        # it might really be a int or float
        # so if string verify!!
        if isinstance(element, str):
            try:
                val = float(element)
            except ValueError:
                # its probably a string
                try:
                    val = parser.parse(element)
                    return datetime
                except ValueError:
                    pass
            return str

            if element.contains("."):
                return float
            else:
                return int
        else:
            # otherwise just return the type of
            return type(element)

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


class DataType:

    def __init__(self, datatype, mean, std, *args, **kwargs):
        pass
