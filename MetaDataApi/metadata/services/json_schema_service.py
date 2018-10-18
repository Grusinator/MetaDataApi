import json
import os
import re
from django.db import transaction
from django.core.files.base import ContentFile
from MetaDataApi.metadata.services.rdfs_service import RdfService
import inflection

# from jsonschema import validate
from urllib import request
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

from schemas.json.omh.schema_names import schema_names
from .base_functions import BaseMetaDataService


class JsonSchemaService(BaseMetaDataService):

    def __init__(self):
        super(JsonSchemaService, self).__init__()
        self.schema = None
        self.baseurl = None
        self.subtypes = ["oneOf", "allOf", "anyOf"]
        self.skip_fields = [
            "description",
            # "label",
            "$schema",
            "definitions"
        ]
        # self.skip_fields.extend(self.subtypes)

    def load_json_schema(self, input_url, schema_name):
        self.baseurl, filename = self._infer_info_split_url(input_url)
        label = filename.replace(".json", "")

        data = self._read_json_from_url(input_url)

        schema_name = self.standardize_string(
            schema_name, remove_version=False)

        try:
            self.schema = Schema.objects.get(label=schema_name)
        except:
            self.schema = Schema()
            self.schema.label = schema_name
            self.schema.description

            # create a dummy file
            content = ContentFile("")
            self.schema.rdfs_file.save(schema_name + ".ttl", content)
            self.schema.url = self.schema.rdfs_file.url
            self.schema.save()

        return_objects = self._iterate_schema(data, label, filename=filename)

        # just in order to update the media turtle file
        RdfService().export_schema_from_db(self.schema.label)

        return self._objects_created_list

    def write_to_db_baseschema(self):
        baseurl = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas/json/omh/schemas/"

        for name in schema_names:
            obj_list = self.load_json_schema(baseurl + name, "openMHealth")
            print(len(obj_list))

        self._error_list

    def _read_json_from_url(self, url):

        with request.urlopen(url) as resp:

            text = resp.read().decode()

            # validate data
            try:
                data = json.loads(text)
            except Exception as e:
                if text[-5:] == ".json":
                    with request.urlopen(self.baseurl + "/" + text) as resp:
                        text = resp.read().decode()
                        data = json.loads(text)
                else:
                    raise Exception(e)

        return data

    def _infer_info_split_url(self, url):
        filename = url.split("/")[-1]
        baseurl = "/".join(url.split("/")[:-1])

        return baseurl, filename

    def _validate_url(self, url):
        urlmapper = {
            "http://tools.ietf.org/html/rfc3339": None,
            "http://purl.bioontology.org/ontology/SNOMEDCT/7389001": None
        }
        var1 = url in urlmapper
        return urlmapper.get(url) if url in urlmapper else url

    def _filt_type(self, obj_list, object_class):
        return list(
            filter(lambda x: isinstance(x, object_class), obj_list))

    def _get_rel_names(self, objects, property_dict):
        returns = []
        for item, obj_rel_name in zip(objects, property_dict.keys()):
            if isinstance(item, Object):
                returns.append(obj_rel_name)
        return returns

    def _iterate_schema(self, dict_data, root_label, current_object=None,
                        definitions=None, filename=None):

        return_objects = []
        # extend definitions each time
        definitions = dict_data.get("definitions") or definitions

        obj_type = dict_data.get("type")

        description = dict_data.get("description")

        # first figure out if this is a class
        if dict_data.get("type") == "object":

            # create object -  if filename exists name it the filename
            label = filename.replace(".json", "") if filename else root_label
            new_object = self._try_create_item(
                Object(
                    label=label,
                    schema=self.schema,
                    description=description
                )
            )

            # make sure this single element is returned
            return_objects.append(new_object)

            # create the object relation
            if current_object is not None:
                # None is root - so no relation
                obj_rel = ObjectRelation(
                    from_object=current_object,
                    to_object=new_object,
                    schema=self.schema,
                    label=root_label)
                self._try_create_item(obj_rel)

            # update current and parrent object
            parrent_object = current_object
            current_object = new_object

        for key, value in dict_data.items():
            # reference to new schema
            if key in self.skip_fields:
                continue

            elif key in self.subtypes:
                # assuming the value is a list of dicts then
                for off_dict in value:
                    new_objects = self._iterate_schema(
                        off_dict, root_label, current_object, definitions)
                    return_objects.extend(new_objects)

            elif key == "$ref":
                if value[0] is "#":
                    def_name = value.split("/")[-1]
                    definition = definitions[def_name]
                    if "$ref" in definition:
                        url = self.baseurl + "/" + \
                            definition["$ref"]
                    elif "references" in definition:
                        continue
                    else:
                        continue
                        # skip references
                        # url = definition.get("references")[0].get("url")

                else:
                    url = self.baseurl + "/" + value

                url = self._validate_url(url)
                if not url:
                    continue

                # load data and prepare to iterate trough
                new_dict_data = self._read_json_from_url(url)

                # when stepping into a new file the label should be
                # the file name

                _, filename = self._infer_info_split_url(url)
                # definitions is not inherited trough references
                new_objects = self._iterate_schema(
                    new_dict_data, root_label, current_object,
                    filename=filename)
                return_objects.extend(new_objects)

            # only select type if it is not an object type
            elif key in ["value", "type"] and value != "object":
                # this is an attribute

                # try to find the relevant attribute date
                unit = dict_data.get("unit")
                data_type = dict_data.get("type")
                description = dict_data.get("description")
                if isinstance(value, dict):
                    unit = value.get("unit") or unit
                    data_type = value.get("type") or data_type
                    description = value.get("description") or description

                # here we just create it and return it
                # saving is done after the object has been created
                # if this dict contains "other classes"
                attribute = self._try_create_item(
                    Attribute(
                        label=root_label,
                        datatype=data_type,
                        description=description,
                        object=current_object
                    )
                )

                # consider saving here if it gets an object with
                return_objects.append(attribute)

            # this is an attribute, but if we allready have an attribute in the
            # return object, add these info to that one, else just create one maybe
            elif key == "unit":
                pass
            elif key == "enum":
                pass

            elif key == "properties":

                new_objects = self._iterate_schema(
                    value, root_label, current_object, definitions)

            elif isinstance(value, dict):
                new_objects = self._iterate_schema(
                    value, key, current_object, definitions)
                return_objects.extend(new_objects)

        # here we identify if the structure should be simplified: to avoid
        # fx unit value objects attributes. If there is one class related
        # to only one attribute. then remove the class and make the
        # object relation a attribute label to the attribute
        # this should only be tested each time we are finished with an object

        # same test as earlier
        if dict_data.get("type") == "object":
            # fiugre out if this object only has one attribute and no relations
            atts = Attribute.objects.filter(object=current_object).count()
            rels = ObjectRelation.objects.filter(
                from_object=current_object).count()
            if atts == 1 and rels == 0:
                # simplify
                attribute = Attribute.objects.get(object=current_object)

                # use parrent object as object instead
                if parrent_object is None:
                    # if None, consider delete object. attribute must have
                    # object
                    # or keep is as it is, to avoid deleting single object
                    # attribute relations
                    pass

                else:
                    # continue the process
                    attribute.object = parrent_object
                    attribute.description += " -> simplified: " + root_label
                    self._try_create_item(attribute, update=True)
                    current_object.delete()

                    # return as if it was an attribute, which it now is
                    return_objects = [attribute, ]

        # we return the created objects from this branch in order
        # to create the object relations
        return return_objects