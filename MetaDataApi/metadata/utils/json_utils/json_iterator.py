from abc import ABCMeta, abstractmethod


class IJsonIterator:
    __metaclass__ = ABCMeta

    att_types = (str, int, float, bool)

    @abstractmethod
    def __init__(self):
        self.depth = 0

    @abstractmethod
    def handle_attributes(self, parrent_object,
                          data, label: str):
        raise NotImplementedError

    @abstractmethod
    def handle_objects(self, parrent_object, data, label: str):
        raise NotImplementedError

    @abstractmethod
    def handle_schema_edges(self, parrent_object, data, label: str):
        raise NotImplementedError

    def isAnAttribute(self, value):
        return isinstance(value, self.att_types) or (
                isinstance(value, dict) and
                self.dict_contains_only_attr_values(value)
        )

    def iterate_json_tree(self, input_data, parrent_object=None):
        self.depth += 1
        if input_data is None:
            self.depth -= 1
            return

        if isinstance(input_data, list):
            for elm in input_data:
                self.iterate_json_tree(
                    elm, parrent_object)

            self.depth -= 1
            return
        # it must be some sort of value, this might only happen
        # if the parrent structure is a list, because if it is a dict
        # the value of the dict is tested for being an attribute
        elif not isinstance(input_data, dict):
            if parrent_object is not None:
                self.handle_attributes(parrent_object, input_data, None)
            self.depth -= 1
            return

        elif isinstance(input_data, dict):
            for key, value in input_data.items():
                if self.isAnAttribute(value):
                    self.handle_attributes(parrent_object, value, key)
                else:
                    obj = self.handle_objects(parrent_object, value, key)

                    obj_rel = self.handle_schema_edges(
                        parrent_object, obj, None)

                    self.iterate_json_tree(
                        value, parrent_object=obj or parrent_object)

        self.depth -= 1
        return

    def dict_contains_only_attr_values(self, data):
        # if its not a dict, then its not an
        # attribute
        if not isinstance(data, dict):
            return False

        data = data.copy()
        if len(data) == 0:
            return False
        attr_names = ["value", "unit"]
        attrs = [data.pop(name, None) for name in attr_names]

        return len(data) == 0
