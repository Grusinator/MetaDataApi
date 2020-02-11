from dataproviders.services.transform_methods.regex_patterns import REPattern


def transform_nested_data_structure_keys(data, transform_method):
    method_mapper = {dict: _iterate_dict_and_transform, list: _iterate_list_and_transform}
    method = method_mapper.get(type(data))
    return method(data, transform_method) if method else data


def clean_invalid_key_chars(data):
    def transform_method(string):
        string = REPattern.multiple_whitespaces.replace('_', string)
        string = REPattern.special_characters.replace("X", string)
        string = REPattern.trailing_underscore.remove(string)
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
