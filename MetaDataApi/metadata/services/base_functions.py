import os
import re
import inflection
# from jsonschema import validate
from urllib import request
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

from schemas.json.omh.schema_names import schema_names
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from service_objects.services import Service
import uuid


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
