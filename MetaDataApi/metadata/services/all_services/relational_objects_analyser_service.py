from urllib import request

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from inflection import underscore

from metadata.models import Attribute, Object, ObjectRelation, ObjectInstance, StringAttributeInstance
from metadata.services import BaseMetaDataService


class RelationalObjectsAnalyserService():

    def connect_objects_to_foaf(self, objects):
        foaf = BaseMetaDataService.get_foaf_person()
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
            base_object, BaseMetaDataService.get_foaf_person(), discovered_objects=[])

        return foaf_found

    def iterate_find_related_obj(self, parrent_obj, find_obj,
                                 discovered_objects=[]):
        if isinstance(parrent_obj, (ObjectInstance,
                                    StringAttributeInstance)):
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

        # data_type is only used in case of attributes
        if isinstance(obj, Attribute) and data_type:
            v2 = self.data_type_match(obj, data_type)
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

    def data_type_match(self, object, data_type):
        return 0

    def relations_match(self, object, json_desendents, json_parrent):
        """
        check if there are similarities with the structure
        """
        return 0
