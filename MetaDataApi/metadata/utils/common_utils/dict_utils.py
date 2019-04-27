
class DictUtils:

    @staticmethod
    def inverse_dict(dictionary: dict, value: str):
        try:
            keys = list(dictionary.keys())
            values = list(dictionary.values())
            index = values.index(value)
            return keys[index]
        except Exception as e:
            raise Exception("could not find key of value: %s in dict: %s" % (value, str(dictionary)))
