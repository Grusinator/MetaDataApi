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

        modified_data = self.iterate_data(input_data, person)

        serialized_data = self.serialize_objects(modified_data)

        return serialized_data

    def serialize_objects(self, object_list):
        # TODO: implement real serialization
        dummy_string = ', '.join(str(x) for x in object_list)

        return dummy_string

    def iterate_data(self, input_data, parrent_obj_inst):
        # for each branch in the tree check match for labels,
        # attribute labels and relations labels

        instance_list = []

        for key, value in input_data.items():
            # this is likely a object if it contains other
            # attributes or objects
            if isinstance(value, dict):
                # test if value dict only contains
                # "value", "unit" and whatever attr
                if self.dict_contains_only_attr(value):
                    look_only_for = [Attribute, ]

                    # check if the key is a label
                    att = self.find_label_in_metadata(
                        key, value, look_only_for_items=look_only_for)

                    if isinstance(att, Attribute):
                        instance_list.append(
                            GenericAttributeInstance(
                                base=att,
                                object=parrent_obj_inst,
                                value=value.get("value")
                            )
                        )
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
                        # test if relation between parrent exists
                        obj_rel = self.relation_between_objects(
                            parrent_obj_inst, obj)

                        # create object instance of the one found from label
                        obj_inst = instance_list.append(
                            ObjectInstance(
                                base=obj
                            )
                        )

                        # if relation exist create instance
                        if obj_rel:
                            parrent_obj_inst = ObjectRelationInstance(
                                from_obj=parrent_obj_inst,
                                to_obj=obj_inst,
                            )
                            instance_list.append(parrent_obj_inst)

                    elif isinstance(obj, ObjectRelation):
                        # dont act here, it should be created when
                        # an object is identified

                        # just step down
                        pass

                    # then iterate down the object value
                    # to find connected objects
                    returned_objects = self.iterate_data(
                        value, parrent_obj_inst)
                    instance_list.extend(returned_objects)

            # this must be an attribute
            elif isinstance(value, (str, int, float)):
                # it is probably an attribute
                data_type = self.identify_datatype(value)
                att = self.find_label_in_metadata(
                    key, data_type, look_only_for_items=[Attribute, ])

                if att:
                    instance_list.append(
                        AttributeInstance(
                            base=att,
                            object=parrent_obj_inst,
                            value=str(value)
                        )
                    )

        # when all objects are mapped return the instances
        return instance_list

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
