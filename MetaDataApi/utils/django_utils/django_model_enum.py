from enum import Enum


class DjangoModelEnum(Enum):
    @classmethod
    def build_choices(cls) -> list:
        return [(element.value, element.value) for element in cls]
