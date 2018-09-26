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

        navigation_dict = {filename: data, }
        while navigation_dict.count is not 0:
            nav_object = navigation_dict.pop()
            for key, value in nav_object.items():
                if isinstance(value, dict):
                    navigation_dict[key] = value
                    continue
