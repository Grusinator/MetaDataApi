import json
import os
# from jsonschema import validate
from urllib import request
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)


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
        self.skip_fields.extend(self.subtypes)
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

    def infer_schema_info_from_url(self, url):
        filename = url.split("/")[-1]
        baseurl = "/".join(url.split("/")[:-1])

        return baseurl, filename

    def create_object_relations(self, object, new_objects):
        for new_object in new_objects:
            label = "%s has %s" % (object.label, new_object.label)
            obj_rel = ObjectRelation(
                from_object=object,
                to_object=new_object,
                url=self.schema.url,
                label=label)
            obj_rel.save()
            # to check the objects that have been create
            self._debug_objects_list.append(obj_rel)

    def create_attributes(self, no_obj_attributes, current_object):
        for no_obj_attribute in no_obj_attributes:
            no_obj_attribute.object = current_object
            try:
                no_obj_attribute.save()
            except Exception as e:
                # most likey if it allready exists
                pass

            # to check the objects that have been create
            self._debug_objects_list.append(no_obj_attribute)
        return no_obj_attributes

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

    def identify_properties(self, dict_data, root_label, current_object=None,
                            definitions=None):

        return_objects = []
        # extend definitions each time
        definitions = dict_data.get("definitions") or definitions

        obj_type = dict_data.get("type")

        description = dict_data.get("description")

        # first figure out if this is a class
        if dict_data.get("type") == "object":
            current_object = Object(
                label=root_label,
                schema=self.schema,
                description=description)
            current_object.save()
            # to check the objects that have been create
            self._debug_objects_list.append(current_object)

        # this basicly ignores the oneof.. etc. structure
        subdata = [dict_data.get(subtype) for subtype in self.subtypes]
        if any(subdata):
            # get first that is not none
            subdata = next(d for d in subdata if d is not None)
            # merge list of dict to one dict
            subdata = dict(pair for d in subdata for pair in d.items())
            dict_data.update(subdata)
            # consider pop the sub list element

        for key, value in dict_data.items():
            # reference to new schema
            if key in self.skip_fields:
                continue

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

                _, filename = self.infer_schema_info_from_url(url)
                label = filename.replace(".json", "")
                # definitions is not inherited trough references
                new_objects = self.identify_properties(
                    new_dict_data, label, current_object)
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

                # if we have allready found an attribute
                if len(self.filt_type(return_objects, Attribute)):
                    attribute = next(self.filt_type(return_objects, Attribute))
                    # update missing info
                    attribute.datatype = attribute.datatype or data_type
                    attribute.description = attribute.description or description
                    # root label should be okay
                else:
                    # here we just create it and return it
                    # saving is done after the object has been created
                    # if this dict contains "other classes"
                    attribute = Attribute(
                        label=root_label,
                        datatype=data_type,
                        description=description,
                        object=current_object
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

                new_objects = self.identify_properties(
                    value, root_label, current_object, definitions)

                # by iterating though properties we dont know if it is an object
                # or just an attribute (if it only has unit and value)

                no_obj_attributes = self.filt_type(new_objects, Attribute)
                objects = self.filt_type(new_objects, Object)

                # it is an attribute
                if len(no_obj_attributes) >= 1 and len(objects) == 0:
                    attributes = self.create_attributes(
                        no_obj_attributes, current_object)
                    # return_objects.extend(attributes)

                    # if this is caracterized as attrbute
                    # it cannot be a class, maybe return instead
                    continue

                # this is an object, so lets create it
                if len(new_objects):
                    # we know this is an object because it has properties
                    current_object = Object(
                        label=root_label,
                        schema=self.schema,
                        description=description)
                    current_object.save()
                    # to check the objects that have been create
                    self._debug_objects_list.append(current_object)

                    # newly discovered objects should be added to return list
                    return_objects.append(current_object)

                    # create the object relations with the current and the returned objects
                    self.create_object_relations(current_object, objects)

                # if there is no object this is a dead end. we dont want to create an object
                # this also means that objects that have no attributes will not be created
                # consider if this is what we want.

                continue

            elif isinstance(value, dict):
                if len(self._debug_objects_list) >= 3:
                    pass

                new_objects = self.identify_properties(
                    value, key, current_object, definitions)
                return_objects.extend(new_objects)

        # we return the created objects from this branch in order
        # to create the object relations
        return return_objects

    def load_json_schema(self, url, schema_name):
        self.baseurl, filename = self.infer_schema_info_from_url(url)
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

        description = data.get("description")

        first_object = Object(
            label=label,
            schema=self.schema,
            description=description)
        first_object.save()

        self.identify_properties(data, label, first_object)

        # data = self.read_json_from_url(url)

        # navigation_dict = {filename: data}
        # while len(navigation_dict) is not 0:
        #     #
        #     _, nav_object = navigation_dict.popitem()

        #     for key, value in nav_object.items():

        #         if key is "properties":
        #             # figure out if it really is a property or a new class

        #             # if the element is a dict traverse it later
        #         if isinstance(value, dict):
        #             navigation_dict[key] = value
        #             continue
        #         # if element is a reference to another file
        #         elif key is "$ref":
        #             ref_url = baseurl + value
        #             ref_data = self.read_json_from_url(ref_url)
        #             navigation_dict[value] = ref_data

        #         elif key is "definitions":

        #         elif isinstance(value, str):
        #             pass
