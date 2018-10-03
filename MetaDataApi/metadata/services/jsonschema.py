import json
import os
# from jsonschema import validate
from urllib import request
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

from schemas.json.omh.schema_names import schema_names


class JsonSchemaService():

    def __init__(self):
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
        self._debug_objects_list = []

    def read_json_from_url(self, url):

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

    def infer_info_split_url(self, url):
        filename = url.split("/")[-1]
        baseurl = "/".join(url.split("/")[:-1])

        return baseurl, filename

    def create_object_relations(self, b_object, new_objects, rel_name=None):
        rel_names = rel_name or ["has" for i in range(len(new_objects))]
        for new_object, rel_name in zip(new_objects, rel_names):
            if isinstance(new_object, Object):
                obj_rel = ObjectRelation(
                    from_object=b_object,
                    to_object=new_object,
                    url=self.schema.url,
                    label=rel_name)
                obj_rel.save()
                # to check the objects that have been create
                self._debug_objects_list.append(obj_rel)

    def validate_url(self, url):
        urlmapper = {
            "http://tools.ietf.org/html/rfc3339": None,
            "http://purl.bioontology.org/ontology/SNOMEDCT/7389001": None
        }
        var1 = url in urlmapper
        return urlmapper.get(url) if url in urlmapper else url

    def filt_type(self, obj_list, object_class):
        return list(
            filter(lambda x: isinstance(x, object_class), obj_list))

    def get_rel_names(self, objects, property_dict):
        returns = []
        for item, obj_rel_name in zip(objects, property_dict.keys()):
            if isinstance(item, Object):
                returns.append(obj_rel_name)
        return returns

    def iterate_schema(self, dict_data, root_label, current_object=None,
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
            new_object = Object(
                label=label,
                schema=self.schema,
                description=description)
            new_object.save()
            # to check the objects that have been create
            self._debug_objects_list.append(new_object)

            # make sure this single element is returned
            return_objects.append(new_object)

            # create the object relation
            if current_object is not None:
                # None is root - so no relation
                obj_rel = ObjectRelation(
                    from_object=current_object,
                    to_object=new_object,
                    url=self.schema.url,
                    label=root_label)
                obj_rel.save()
                # to check the objects that have been create
                self._debug_objects_list.append(obj_rel)

            # update current object
            current_object = new_object

        for key, value in dict_data.items():
            # reference to new schema
            if key in self.skip_fields:
                continue

            elif key in self.subtypes:
                # assuming the value is a list of dicts then
                for off_dict in value:
                    new_objects = self.iterate_schema(
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
                        # skip references
                        # url = definition.get("references")[0].get("url")

                else:
                    url = self.baseurl + "/" + value

                url = self.validate_url(url)
                if not url:
                    continue

                # load data and prepare to iterate trough
                new_dict_data = self.read_json_from_url(url)

                # when stepping into a new file the label should be
                # the file name

                _, filename = self.infer_info_split_url(url)
                # definitions is not inherited trough references
                new_objects = self.iterate_schema(
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
                attribute = Attribute(
                    label=root_label,
                    datatype=data_type,
                    description=description,
                    object=current_object
                )
                attribute.save()
                # to check the objects that have been create
                self._debug_objects_list.append(attribute)

                # consider saving here if it gets an object with
                return_objects.append(attribute)

            # this is an attribute, but if we allready have an attribute in the
            # return object, add these info to that one, else just create one maybe
            elif key == "unit":
                pass
            elif key == "enum":
                pass

            elif key == "properties":

                new_objects = self.iterate_schema(
                    value, root_label, current_object, definitions)

                # relation_names = self.get_rel_names(new_objects, value)
                # # create the object relations with the current and the new_objects
                # self.create_object_relations(
                #     current_object, new_objects, relation_names)

            elif isinstance(value, dict):
                new_objects = self.iterate_schema(
                    value, key, current_object, definitions)
                return_objects.extend(new_objects)

        # we return the created objects from this branch in order
        # to create the object relations
        return return_objects

    def load_json_schema(self, url, schema_name):
        self.baseurl, filename = self.infer_info_split_url(url)
        label = filename.replace(".json", "")
        try:
            self.schema = Schema.objects.get(label=schema_name)
        except:
            self.schema = Schema(
                label=schema_name,
                url=self.baseurl,
            )
            self.schema.save()

        data = self.read_json_from_url(url)

        return_objects = self.iterate_schema(data, label, filename=filename)

        return self._debug_objects_list

    def create_default_schemas(self):
        baseurl = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas/json/omh/schema/"

        for name in schema_names:
            obj_list = self.load_json_schema(baseurl + name)
            print(len(obj_list))
