
class DictUtils:

    @staticmethod
    def inverse_dict(dicti, value):
        try:
            keys = list(dicti.keys())
            values = list(dicti.values())
            index = values.index(value)
            return keys[index]
        except Exception as e:
            return None
