import json
from typing import Union

JsonType = Union[dict, list]


class JsonUtils:

    @staticmethod
    def validate(text: str) -> JsonType:
        return json.loads(text)

    @staticmethod
    def clean(text: str) -> str:
        json_obj = json.loads(text)
        return json.dumps(json_obj, indent=4)
