import re
from enum import Enum


class REPattern(Enum):
    long_id = "([0-9]{6,})"
    guid = "[0-9a-fA-F]{8,}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
    guid_like = "[0-9a-fA-F]{12,}"
    multiple_whitespaces = ' +'
    multiple_underscore = '_+'
    special_characters = "[^\w\*]"
    trailing_underscore = "^_+|_+$"
    trailing_whitespace = "^ +| +$"

    def replace(self, replacement, string: str):
        return re.sub(self.value, replacement, string)

    def remove(self, string: str):
        return self.replace("", string)
