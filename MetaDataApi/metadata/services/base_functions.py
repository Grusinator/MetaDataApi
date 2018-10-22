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

    def _try_get_item(self, item_type, label):
        try:
            # this "with transaction.atomic():"
            # is used to make tests run due to some
            # random error, atomic something.
            # it works fine when runs normally

            with transaction.atomic():
                return item_type.objects.get(label=label)

        except ObjectDoesNotExist as e:
            # try create object
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
                return_item = item_type.objects.get(label=item.label)
                if update or self.overwrite_db_objects:
                    if self.save_to_db:
                        return_item.delete()
                        item.save()
                    # return the saved item instead of the fetched one
                    # that is now deleted
                    return_item = item

            # on update add to debug list
            self._objects_created_list.append(item)
            return return_item

        except ObjectDoesNotExist as e:
            # try create object
            try:
                if self.save_to_db:
                    item.save()
                self._objects_created_list.append(item)
                return item
            except Exception as e:
                self._error_list.append(str(e))
                return None

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
        schema = Schema.objects.get(label="friend_of_a_friend_(foaf)")
        find_obj = Object.objects.get(label="person", schema=schema)
        return find_obj
