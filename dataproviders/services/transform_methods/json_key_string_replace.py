from dataproviders.services.transform_methods.regex_patterns import REPattern


def clean_invalid_key_chars(data):
    def key_transform(key: str):
        key = REPattern.multiple_whitespaces.replace('_', key)
        key = REPattern.special_characters.remove(key)
        key = REPattern.trailing_underscore.remove(key)
        return key

    def value_transform(value):
        if isinstance(value, str):
            value = REPattern.multiple_whitespaces.replace(' ', value)
            value = REPattern.trailing_whitespace.remove(value)
        return value

    return transform_nested_data_structure(data, key_transform, value_transform)


def transform_nested_data_structure(data, key_transform, value_transform):
    method_mapper = {dict: _iterate_dict_and_transform, list: _iterate_list_and_transform}
    method = method_mapper.get(type(data))
    return method(data, key_transform, value_transform) if method else value_transform(data)


def _iterate_list_and_transform(list_structure, key_transform, value_transform):
    return [transform_nested_data_structure(elm, key_transform, value_transform) for elm in list_structure]


def _iterate_dict_and_transform(dict_structure, key_transform, value_transform):
    for key, value in dict_structure.copy().items():
        new_key = key_transform(key)
        dict_structure[key] = transform_nested_data_structure(value, key_transform, value_transform)
        if new_key != key:
            dict_structure[new_key] = dict_structure.pop(key)
    return dict_structure
