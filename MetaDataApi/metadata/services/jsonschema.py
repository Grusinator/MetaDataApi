import json
from jsonschema import validate


class JsonSchemaService():

    def load_json_schema(self, url):
        filename = url.split("/")[-1]
        root = json.loads(url)
