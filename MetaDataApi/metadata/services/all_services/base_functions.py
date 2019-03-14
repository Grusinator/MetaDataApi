import re
from datetime import datetime

import dateutil
import inflection
from django.core.exceptions import (
    ObjectDoesNotExist, MultipleObjectsReturned)
from django.core.files.base import ContentFile
from django.db import transaction

from metadata.models import (
    ObjectInstance, ObjectRelationInstance,
    StringAttributeInstance,
    DateTimeAttributeInstance, BoolAttributeInstance,
    FloatAttributeInstance, IntAttributeInstance
)
# from jsonschema import validate
from metadata.models import (
    Schema, Object, Attribute, ObjectRelation)


class BaseMetaDataService():

    def __init__(self):
        # super(BaseMetaDataService, self).__init__()
        self.schema = None
        self.baseurl = None
        self.foaf_person = None

        self.added_meta_items = []
        self.touched_meta_items = []
        self.added_instance_items = []
        self._error_list = []
        # one switch to force overwrite the objects when
        self.overwrite_db_objects = False
        # -- same -- but to disable saving to db
        self.save_to_db = True

        # dont use the same if it allready exists
        self.allways_create_new = False

        self.att_inst_to_type_map = {
            #  StringAttributeInstance: str,
            StringAttributeInstance: str,
            DateTimeAttributeInstance: datetime,
            FloatAttributeInstance: float,
            IntAttributeInstance: int,
            BoolAttributeInstance: bool
        }

        self.att_types = tuple(typ if isinstance(typ, type) else type(typ)
                               for typ in Attribute.data_type_map.keys())

        self.att_instances = tuple(self.att_inst_to_type_map.keys())

        self.instances = self.att_instances + \
                         (ObjectInstance, ObjectRelationInstance)

    def inverse_dict(self, dicti, value):
        try:
            keys = list(dicti.keys())
            values = list(dicti.values())
            index = values.index(value)
            return keys[index]
        except Exception as e:
            return None

    def standardize_string(self, string, remove_version=False):
        string = inflection.underscore(str(string))
        string = string.replace(".json", "")

        string = string.replace(" ", "_")

        # remove any version numbers
        if remove_version:
            string = re.sub(
                r"(|_version|_v|_v.)(|_)\d+\.(\d+|x)(|_)", '', string)

        string = re.sub("(|_)vocabulary(|_)", '', string)

        # remove parenthesis with content
        string = re.sub(r'(|_)\([^)]*\)', '', string)

        # remove trailing and leading whitespace/underscore
        # string = re.sub('/^[\W_]+|[\W_]+$/', '', string)

        return string

    def rest_endpoint_to_label(self, endpoint):
        # TODO the last might not be the most relevant
        endpoint_without_args = endpoint.split("?")[0]
        last_elm = endpoint_without_args.split("/")[-1]
        return self.standardize_string(last_elm)

    def create_new_empty_schema(self, schema_label):
        self.schema = Schema()
        self.schema.label = self.standardize_string(schema_label)
        self.schema.description = ""
        self.schema.url = "temp"
        # quick fix for saving without conflicting with unique url

        # create a dummy file
        content = ContentFile("")
        self.schema.rdfs_file.save(schema_label + ".ttl", content)
        self.schema.url = self.schema.rdfs_file.url
        self.schema.save()

        self.touched_meta_items.append(self.schema)

        return self.schema

    def is_meta_item_in_created_list(self, item, item_list=None):
        item_list = item_list or self.touched_meta_items

        # new __eq__implementation
        return next(filter(item.__eq__, item_list), None)

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

        # def compare_rel(
        #     x): return x.from_relations in item.from_relations.all()

        # def func(x): return any(filter(compare_rel, x.from_relations.all()))
        # any([func(x) for x in same_labels])

        # else:

    def identify_data_type(self, element):
        if element is None:
            return None

        def test_float(elm):
            assert ("." in elm), "does not contain decimal separator"
            return float(elm)

        def test_bool(elm):
            trues = ("true", "True")
            falses = ("false", "False")

            if elm in trues:
                return True
            elif elm in falses:
                return False
            else:
                raise ValueError("is not either true or false")

        def test_datetime(text):
            try:
                return dateutil.parser.parse(text)
            except:

                datetime_formats = (
                    '%Y-%m-%dT%H: %M: %SZ',  # strava
                )

                for fmt in datetime_formats:
                    try:
                        return datetime.strptime(text, fmt)
                    except ValueError as e:
                        pass

                raise ValueError('no valid date format found')

        # even though it is a string,
        # it might really be a int or float
        # so if string verify!!
        if isinstance(element, str):
            conv_functions = {
                float: test_float,
                int: lambda elm: int(elm),
                datetime: test_datetime,
                str: lambda elm: str(elm),
                bool: test_bool
            }

            order = [float, int, datetime, bool, str]

            for typ in order:
                try:
                    # try the converting function of that type
                    # if it doesnt fail, thats our type
                    return conv_functions[typ](element)
                except (ValueError, AssertionError) as e:
                    pass

            # if nothing else works, return as string
            return str(element)

        elif isinstance(element, (float, int, bool)):
            # otherwise just return the type of
            return element

    def do_instance_exists(self, instance):
        search_args = {"pk": instance.pk}
        return self.find_item(instance, search_args)

    def do_meta_item_exists(self, item, parrent_label=None):

        item.label = self.standardize_string(item.label)
        search_args = self.build_search_args_for_meta_items(item, parrent_label)
        return self.find_item(item, search_args)

    def find_item(self, item, search_args):
        item_type = type(item)
        try:
            # this "with transaction.atomic():"
            # is used to make tests run due to some
            # random error, atomic something.
            # it works fine when runs normally

            with transaction.atomic():
                return item_type.objects.get(**search_args)

        except ObjectDoesNotExist as e:
            return None
        except MultipleObjectsReturned as e:
            self._error_list.append((item, e))
            if hasattr(item, "schema"):
                schema_label = item.schema.label
            else:
                schema_label = item.object.schema.label
            print("""Warning, this is most likely wrong wrong, the object
                found:  %s  objects, but the first was chosen.
                -- label: %s schema: %s""" % (
                item_type.objects.filter(**search_args).count(),
                item.label,
                schema_label,
            ))

            return item_type.objects.filter(**search_args).first()

        except Exception as e:
            pass

    def _try_create_item(self, item, update=False, parrent_label=None):

        item_type = type(item)
        remove_version = not isinstance(item_type, Schema)

        # test if exists
        item.label = self.standardize_string(
            item.label, remove_version=remove_version)
        try:
            # this "with transaction.atomic():"
            # is used to make tests run due to some
            # random error, atomic something.
            # it works fine when runs normally
            with transaction.atomic():

                # we want to be able to tell uniquely if this is the same
                # object, so test on all objects, not only the label,
                # so that it is possible to know if we are overwriting
                # objects that shouldnt
                return_item = self.do_meta_item_exists(
                    item, parrent_label=parrent_label)

                # the object exists,
                if return_item:
                    if update or self.overwrite_db_objects:
                        if self.save_to_db:
                            return_item.delete()
                            item.save()

                        else:
                            # if not updated, return the fetched one
                            item = return_item
                    else:
                        item = return_item
                # does not exists, create it!
                else:
                    try:
                        if self.save_to_db:
                            item.save()
                            self.added_meta_items.append(item)

                    except Exception as e:
                        # on update add to debug list
                        self._error_list.append((item, e))
                        return None

            # on success return the item, either fetched, or saved
            # so that the referenced object lives in the database
            self.touched_meta_items.append(item)
            return item

        except (transaction.TransactionManagementError,) as e:
            return None
        except Exception as e:
            return None

    def is_objects_connected(self, obj_from, obj_to, objects):
        relations = obj_from.from_relations.all()

        related_objects = list(map(lambda x: x.to_object.get(), relations))

        related_objects = list(filter(lambda x: x in objects, related_objects))

        for obj in related_objects:
            if obj == obj_to:
                return True
            elif self.is_objects_connected(obj, obj_to, objects):
                return True

        return False

    def get_foaf_person(self):
        if not self.foaf_person:
            schema = Schema.objects.get(label="friend_of_a_friend")
            self.foaf_person = Object.objects.get(
                label="person", schema=schema)
        return self.foaf_person

    def att_to_att_inst(self, attr):
        data_type = self.inverse_dict(Attribute.data_type_map, attr.data_type)

        return self.inverse_dict(self.att_inst_to_type_map, data_type)

    def get_connected_attribute_pairs(self, att_1, att_2):

        foaf1, att1_list = BaseMetaDataService.path_to_object(
            att_1, self.get_foaf_person(), childrens=[])

        foaf2, att2_list = BaseMetaDataService.path_to_object(
            att_2, self.get_foaf_person(), childrens=[])

        # get first common object
        common_set = set(att1_list) & set(att2_list)
        common_obj = next(filter(lambda x: x in common_set, att1_list))

        # truncate list down to common object
        att1_list = att1_list[:att1_list.index(common_obj) + 1]
        att2_list = att2_list[:att2_list.index(common_obj) + 1]

        returns = []

        common_instances = ObjectInstance.objects.filter(base=common_obj)
        for common_instance in common_instances:
            value1 = self.get_specific_child(
                common_instance, att_1, path=att1_list)
            value2 = self.get_specific_child(
                common_instance, att_2, path=att2_list)
            returns.append((value1, value2))

        return returns

    def get_specific_child(self, obj_inst, child, path=None):
        """
        get a decendent object, either att, or obj of a specific type
        """
        if path is None:
            path = self.path_to_object(child, obj_inst.base)

        search_args = self.build_search_args_from_list(path, obj_inst)
        AttributeInstance = self.att_to_att_inst(child)
        try:
            return AttributeInstance.objects.get(**search_args)
        except ObjectDoesNotExist as e:
            return None
        except MultipleObjectsReturned as e:
            print("WARNING: obj, contains multiple object, first is taken")
            return next(AttributeInstance.objects.filter(**search_args))

    def build_search_args_from_list(self, path, obj_inst):
        search_args = {}
        base_arg_name = "from_relations__from_object__"
        arg_name = ""
        # loop though all but last
        for obj in path:
            if isinstance(obj, Attribute):
                arg_name += "object__"
                search_args["base__label"] = obj.label
            elif obj == obj_inst.base:
                # last elm add primary key
                search_args[arg_name + "pk"] = obj_inst.pk
            else:
                # Not neccesary as long as pk is being added
                # search_args[arg_name + "base__label"] = obj.label
                arg_name += base_arg_name

        return search_args

    @staticmethod
    def path_to_object(obj, root_obj, childrens=[]):
        if isinstance(obj, Attribute):
            # add to path
            childrens.append(obj)
            obj = obj.object
        if obj == root_obj:
            return obj, childrens
        else:
            parrent_rels = obj.from_relations.all()
            childrens.append(obj)
            for parrent_rel in parrent_rels:
                parrent_obj = parrent_rel.from_object

                obj, childrens = BaseMetaDataService.path_to_object(
                    parrent_obj, root_obj, childrens=childrens)

                if obj == root_obj:
                    return obj, list(childrens)

            # this branch has been exhausted, return none
            return None, childrens

    def build_search_args_for_meta_items(self, item, parrent_label):
        search_args = {"label": item.label}

        if isinstance(item, Attribute):
            search_args["object__label"] = item.object.label

        elif isinstance(item, Object):
            search_args["schema"] = item.schema
            # adds the option to search for objects dependent
            # on from relations
            if parrent_label and parrent_label == "None":
                search_args["from_relations"] = None
            elif parrent_label:
                search_args["from_relations__from_object__label"] \
                    = parrent_label

        elif isinstance(item, ObjectRelation):
            search_args["from_object"] = item.from_object
            search_args["to_object"] = item.to_object

        return search_args
