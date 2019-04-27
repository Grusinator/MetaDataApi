import json
from typing import Union

JsonType = Union[dict, list]


class JsonUtils:

    @classmethod
    def read_json_file(cls, filename):
        with open(filename, encoding='utf-8') as f:
            return cls.validate(f.read())

    @staticmethod
    def validate(text: str) -> JsonType:
        return json.loads(text)

    @staticmethod
    def clean(text: str) -> str:
        json_obj = json.loads(text)
        return json.dumps(json_obj, indent=4)
