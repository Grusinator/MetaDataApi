from abc import ABC


class BaseUrlArgValue(ABC):
    def __init__(self, value):
        self.value = value
