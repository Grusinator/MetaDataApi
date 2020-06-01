from enum import Enum

ENUM_NAME = "enum_value"


class DjangoModelEnum(Enum):

    @classmethod
    def build_choices(cls) -> list:
        # this has been reversed so that the name is the short one stored in db, it should still be readable
        # the value is then the one that the use will see in the front
        return [(element.get_value(), element.get_value()) for element in cls]

    def get_value(self):
        if not isinstance(self.value, (str, type(None))):
            if hasattr(self.value, ENUM_NAME):
                return getattr(self.value, ENUM_NAME)
            else:
                return self.value.__name__
        else:
            return self.value

    @classmethod
    def get_class_from_value(cls, value_name):
        values = [element.value for element in cls if element.value and element.value.__name__ == value_name]
        return next(iter(values), None)
