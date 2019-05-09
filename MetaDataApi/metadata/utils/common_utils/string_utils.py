import re

import inflection


class StringUtils:
    @staticmethod
    def standardize_string(string, remove_version=False):
        string = inflection.underscore(str(string))
        string = string.replace(".json", "")

        string = string.replace(" ", "_")

        # remove any version numbers
        if remove_version:
            string = re.sub(
                r"(|_version|_v|_v.)(|_)\d+\.(\d+|x)(|_)", '', string)

        string = re.sub("(|_)vocabulary(|_)", '', string)

        # remove parenthesis with content
        string = re.sub(r'(|_)\([^)]*\)', '', string)

        # remove trailing and leading whitespace/underscore
        # string = re.sub('/^[\W_]+|[\W_]+$/', '', string)

        return string

    @staticmethod
    def is_string_none(string):
        return string == None or string == ""
