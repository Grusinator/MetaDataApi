from enum import Enum

ENUM_NAME = "enum_value"


class DjangoModelEnum(Enum):

    @classmethod
    def build_choices(cls) -> list:
        # this has been reversed so that the name is the short one stored in db, it should still be readable
        # the value is then the one that the use will see in the front
        return [(cls.get_value(element), cls.get_value(element)) for element in cls]

    @classmethod
    def get_value(cls, element: Enum):
        if not isinstance(element.value, (str, type(None))):
            if hasattr(element.value, ENUM_NAME):
                return getattr(element.value, ENUM_NAME)
            else:
                return element.value.__name__
        else:
            return element.value

    @classmethod
    def get_class_from_value(cls, value_name):
        values = [element.value for element in cls if element.value and element.value.__name__ == value_name]
        return next(iter(values), None)
