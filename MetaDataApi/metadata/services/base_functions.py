import os
import re
import inflection
# from jsonschema import validate
from urllib import request
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)
from django.core.files.base import ContentFile

from schemas.json.omh.schema_names import schema_names
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from service_objects.services import Service
import uuid
import dateutil


class BaseMetaDataService():

    def __init__(self):
        # super(BaseMetaDataService, self).__init__()
        self.schema = None
        self.baseurl = None

        self._objects_created_list = []
        self._error_list = []
        # one switch to force overwrite the objects when
        self.overwrite_db_objects = False
        # -- same -- but to disable saving to db
        self.save_to_db = True

        # dont use the same if it allready exists
        self.allways_create_new = False

    def standardize_string(self, string, remove_version=False):
        string = inflection.underscore(str(string))

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

    def create_new_empty_schema(self, schema_name):
        self.schema = Schema()
        self.schema.label = schema_name
        self.schema.description = ""

        # create a dummy file
        content = ContentFile("")
        self.schema.rdfs_file.save(schema_name + ".ttl", content)
        self.schema.url = self.schema.rdfs_file.url
        self.schema.save()

        return self.schema

    def validate_if_metaitem_is_in_list(self, item, item_list):

        same_labels = filter(lambda x: item.label == x.label, item_list)

        if isinstance(item, Object):
            for same_label in same_labels:
                if same_label.to_relations.all().count() == 0:
                    return True
                for relation in same_label.to_relations.all():
                    item_to_relation_objects = [
                        rel.to_object for rel in item.from_relations.all()]
                    if relation.to_object in item_to_relation_objects:
                        return True
        elif isinstance(item, Attribute):
            for same_label in same_labels:
                if same_label.object == item.object:
                    return True
        elif isinstance(item, ObjectRelation):
            for in_list in item_list:
                if in_list.label == item.label:
                    return True
        else:
            raise Exception()

        return False

        # def compare_rel(
        #     x): return x.from_relations in item.from_relations.all()

        # def func(x): return any(filter(compare_rel, x.from_relations.all()))
        # any([func(x) for x in same_labels])

        # else:

    def identify_datatype(self, element):
        # even though it is a string,
        # it might really be a int or float
        # so if string verify!!

        def test_float(elm):

            assert ("." in elm), "does not contain decimal separator"
            return float(elm)

        if isinstance(element, str):
            conv_functions = {
                float: lambda elm: test_float(elm),
                int: lambda elm: int(elm),
                datetime: lambda elm: dateutil.parser.parse(elm),
                str: lambda elm: str()
            }

            order = [float, int, datetime, str]

            for typ in order:
                try:
                    # try the converting function of that type
                    # if it doesnt fail, thats our type
                    return type(conv_functions[typ](element))
                except (ValueError, AssertionError) as e:
                    pass

        elif isinstance(element, (float, int)):
            # otherwise just return the type of
            return type(element)

    def _try_get_item(self, item):

        # allways use the label
        search_args = {
            "label": item.label,
        }

        item_type = type(item)

        if isinstance(item, Attribute):
            search_args["object"] = item.object
        elif isinstance(item, Object):
            search_args["schema"] = item.schema
            # search_args["from_relations"] = item.from_relations
        elif isinstance(item, ObjectRelation):
            search_args["from_object"] = item.from_object
            search_args["to_object"] = item.to_object

        try:
            # this "with transaction.atomic():"
            # is used to make tests run due to some
            # random error, atomic something.
            # it works fine when runs normally

            with transaction.atomic():
                return item_type.objects.get(**search_args)

        except ObjectDoesNotExist as e:
            return None
        except Exception as e:
            pass

    def _try_create_item(self, item, update=False):

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
                return_item = self._try_get_item(item)

                # the object exists,
                if return_item:
                    if update or self.overwrite_db_objects:
                        if self.save_to_db:
                            return_item.delete()
                            item.save()

                        else:
                            # if not updated, return the fetched one
                            item = return_item

                # does not exists, create it!
                else:
                    try:
                        if self.save_to_db:
                            item.save()
                    except Exception as e:
                        # on update add to debug list
                        self._error_list.append((str(e), item))
                        return None

            # on success return the item, either fetched, or saved
            # so that the referenced object lives in the database
            self._objects_created_list.append(item)
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
        schema = Schema.objects.get(label="friend_of_a_friend")
        find_obj = Object.objects.get(label="person", schema=schema)
        return find_obj
