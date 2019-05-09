import json
from typing import Union

JsonType = Union[dict, list]


class JsonUtils:
    encoding = "utf-8"

    @classmethod
    def read_json_file(cls, filename):
        with open(filename, encoding=cls.encoding) as f:
            return cls.validate(f.read())

    @classmethod
    def validate(cls, text: str) -> JsonType:
        return json.loads(text, encoding=cls.encoding)

    @staticmethod
    def clean(text: str) -> str:
        json_obj = json.loads(text)
        return json.dumps(json_obj, indent=4)

    @classmethod
    def to_tuple_set_key_value(cls, json_obj: JsonType):
        if isinstance(json_obj, list):
            return [cls.dict_to_set_of_tuple(elm) for elm in json_obj]
        else:
            return cls.dict_to_set_of_tuple(json_obj)

    @staticmethod
    def dict_to_set_of_tuple(dicti: dict):
        if not isinstance(dicti, dict):
            raise Exception("expected dict")
        return {(key, value) for key, value in dicti.items()}
