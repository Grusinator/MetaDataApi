import json
from jsonschema import validate
from urllib import request


class JsonSchemaService():

    def read_json_from_url(self, url):

        with request.urlopen(url) as resp:
            text = resp.read().decode()
            data = json.loads(text)
        return data

    def infer_schema_info_from_url(self, url):
        filename = url.split("/")[-1]
        baseurl = "/".join(url.split("/")[:-1])

        return baseurl, filename

    def load_json_schema(self, url):
        baseurl, filename = self.infer_schema_info_from_url(url)

        data = self.read_json_from_url(url)

        navigation_dict = {filename: data}
        while len(navigation_dict) is not 0:
            #
            _, nav_object = navigation_dict.popitem()
            for key, value in nav_object.items():

                # if the element is a dict traverse it later
                if isinstance(value, dict):
                    navigation_dict[key] = value
                    continue
                # if element is a reference to another file
                elif key is "$ref":
                    ref_url = baseurl + value
                    ref_data = self.read_json_from_url(ref_url)
                    navigation_dict[value] = ref_data

                elif isinstance(value, str):
                    pass
