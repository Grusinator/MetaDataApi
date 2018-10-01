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
            "label",
            "$schema",
            "type",
            "definitions"
        ]
        self.skip_fields.extend(self.subtypes)

    def read_json_from_url(self, url):

        with request.urlopen(url) as resp:

            text = resp.read().decode()

            # validate data
            try:
                data = json.loads(text)
            except:
                with request.urlopen(self.baseurl + "/" + text) as resp:
                    text = resp.read().decode()
                    data = json.loads(text)

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

    def create_attributes(self, no_obj_attributes, current_object):
        for no_obj_attribute in no_obj_attributes:
            no_obj_attribute.object = current_object
            no_obj_attribute.save()

    def identify_properties(self, dict_data, root_label, current_object=None,
                            definitions=None):

        return_objects = []
        # extend definitions each time
        definitions = dict_data.get("definitions") or definitions

        obj_type = dict_data.get("type")

        description = dict_data.get("description")

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
                    if
                    # FixMe: could be pattern instead of $ref
                    # figure out what to do
                    url = self.baseurl + "/" + definitions[def_name]["$ref"]
                else:
                    url = self.baseurl + "/" + value

                # load data and prepare to iterate trough
                new_dict_data = self.read_json_from_url(url)

                # definitions is not inherited trough references
                new_objects = self.identify_properties(
                    new_dict_data, root_label, current_object)

            # probably a attribute but the one below will handle it
            elif key == "unit":
                pass
            elif key == "enum":
                pass
            elif key == "value":
                # this is an attribute

                # try to find the unit
                unit = dict_data.get("unit")
                data_type = value.get("type")
                description = value.get("description")

                # here we just create it and return it
                # saving is done after the object has been created
                # if this dict contains "other classes"
                attribute = Attribute(
                    label=root_label,
                    datatype=data_type,
                    object=None
                )
                return_objects.append(attribute)

            elif key == "properties":

                new_objects = self.identify_properties(
                    value, root_label, current_object, definitions)

                # by iterating though properties we dont know if it is an object
                # or just an attribute (if it only has unit and value)
                if len(new_objects):
                    no_obj_attributes = list(
                        filter(lambda x: isinstance(x, Attribute), new_objects))
                    objects = list(
                        filter(lambda x: isinstance(x, Object), new_objects))

                    # it is just an attribute
                    if len(no_obj_attributes) == 1 and len(objects) == 0:
                        self.create_attributes(
                            no_obj_attributes, current_object)
                    # this is an object, so lets create it
                    elif len(objects) != 0:
                        # we know this is an object because it has properties
                        current_object = Object(
                            label=root_label,
                            schema=self.schema,
                            description=description)
                        current_object.save()

                        # newly discovered objects should be added to return list
                        return_objects.append(current_object)

                        self.create_object_relations(current_object, objects)

            elif isinstance(value, dict):
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
        self.identify_reference(url)

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
