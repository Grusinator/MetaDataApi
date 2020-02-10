import re


def transform_nested_data_structure_keys(data, transform_method):
    method_mapper = {dict: _iterate_dict_and_transform, list: _iterate_list_and_transform}
    method = method_mapper.get(type(data))
    return method(data, transform_method) if method else data


def clean_invalid_key_chars(data):
    def transform_method(string):
        multiple_whitespaces = ' +'
        string = re.sub(multiple_whitespaces, '_', string)
        special_characters = "[^\w\*]"
        string = re.sub(special_characters, "X", string)
        return string

    return transform_nested_data_structure_keys(data, transform_method)


def _iterate_list_and_transform(list_structure, transform_method):
    return [transform_nested_data_structure_keys(elm, transform_method) for elm in list_structure]


def _iterate_dict_and_transform(dict_structure, transform_method):
    for key, value in dict_structure.copy().items():
        new_key = transform_method(key)
        dict_structure[key] = transform_nested_data_structure_keys(value, transform_method)
        if new_key != key:
            dict_structure[new_key] = dict_structure.pop(key)
    return dict_structure
