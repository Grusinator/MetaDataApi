import json
import os
#from jsonschema import validate
from urllib import request
from MetaDataApi.metadata.models import Schema, Object, Attribute, ObjectRelation


class JsonSchemaService():

    def __init__(self):
        self.schema = None
        self.baseurl = None

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

    def identify_properties(self, properties, definitions, root_label, object):
        objectslist = []
        for key, value in properties.items():
            if isinstance(value, dict):
                new_objects = self.identify_properties(
                    value, definitions, key, object)
            # reference to new schema
            elif key == "$ref":
                if value[0] is "#":
                    def_name = value.split("/")[-1]
                    url = self.baseurl + "/" + definitions[def_name]["$ref"]
                else:
                    url = value

                new_objects = self.identify_reference(url)
            elif key is "value":
                # this is an attribute

                # try to find the unit
                unit = properties.get("unit")
                data_type = value.get("type")
                description = value.get("description")

                attribute = Attribute(
                    label=root_label,
                    datatype=data_type
                )

    def identify_reference(self, url):
        _, filename = self.infer_schema_info_from_url(url)

        data = self.read_json_from_url(url)

        definitions = data.get("definitions")

        obj_type = data.get("type")

        description = data.get("description")

        # this basicly ignores the oneof.. etc. structure
        subtypes = ["oneOf", "allOf", "anyOf"]
        subdata = [data.get(subtype) for subtype in subtypes]
        if any(subdata):
            # get first that is not none
            data = next(d for d in subdata if d is not None)
            # merge list of dict to one dict
            data = dict(pair for d in data for pair in d.items())

        if "properties" in data:
            properties = data["properties"]
            navigation_dict = {filename: properties}

            # we know this is an object because it has properties

            object = Object(
                label=filename,
                schema=self.schema,
                description=description)
            object.save()

            objectlist = self.identify_properties(
                properties, definitions, filename, object)

        # while len(navigation_dict) is not 0:
        #     #
        #     _, nav_object = navigation_dict.popitem()

        #     for key, value in nav_object.items():

        #         if key is "properties":
        #             # figure out if it really is a property or a new class
        #             # here the strategy is to go in depth until another file is found
        #             objectlist = self.identify_properties(
        #                 value, definitions, filename, object)

        #             # if the element is a dict traverse it later
        #         if isinstance(value, dict):
        #             navigation_dict[key] = value
        #             continue
        #         # if element is a reference to another file
        #         elif key is "$ref":
        #             ref_url = self.baseurl + value
        #             ref_data = self.read_json_from_url(ref_url)
        #             navigation_dict[value] = ref_data

    def load_json_schema(self, url, schema_name):
        self.baseurl, filename = self.infer_schema_info_from_url(url)

        try:
            self.schema = Schema.objects.get(label=schema_name)
        except:
            self.schema = Schema(
                label=schema_name,
                url=self.baseurl,
            )
            self.schema.save()

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
