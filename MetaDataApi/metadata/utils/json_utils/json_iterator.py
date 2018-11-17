from abc import ABCMeta, abstractmethod


class IJsonIterator:
    __metaclass__ = ABCMeta

    att_types = (str, int, float, bool)

    @abstractmethod
    def __init__(self):
        self.depth = 0

    # all handle functions should take: parrent_object, data, label
    # as parameters

    @abstractmethod
    def handle_attributes(self): raise NotImplementedError

    @abstractmethod
    def handle_objects(self): raise NotImplementedError

    @abstractmethod
    def handle_object_relations(self): raise NotImplementedError

    def iterate_json_tree(self, input_data, parrent_object=None):
        self.depth += 1
        if input_data is None:
            self.depth -= 1
            return

        if isinstance(input_data, list):
            # if its a list, there is no key, all we can do is to step
            # down but add all the data within to a new list
            # def func(x): return isinstance(x, (dict, list))

            # if any([func(x) for x in input_data]):
            #     pass

            for elm in input_data:
                # if isinstance(elm, (dict, list)):
                self.iterate_json_tree(
                    elm, parrent_object)

            self.depth -= 1
            return
        # it must be some sort of value, this might only happen
        # if the parrent structure is a list, because if it is a dict
        # the value of the dict is tested for being an attribute
        elif not isinstance(input_data, dict):
            if parrent_object is not None:
                self._att_function(parrent_object, input_data,
                                   None)
            self.depth -= 1
            return

        elif isinstance(input_data, dict):
            for key, value in input_data.items():
                # this is likely a object if it contains other
                # attributes or objects

                # this must be an attribute
                # test if value dict only contains
                # "value", "unit" and whatever attr
                if isinstance(value, self.att_types) or \
                        (isinstance(value, dict) and
                         self.dict_contains_only_attr(value)):
                        # it is probably an attribute

                    self.handle_attributes(parrent_object, value, key)

                # its probably a object
                else:
                    obj = self.handle_objects(parrent_object, value, key)

                    obj_rel = self.handle_object_relations(
                        parrent_object, obj, None)

                    # then iterate down the object value
                    # to find connected objects
                    self.iterate_json_tree(
                        value, parrent_object=obj or parrent_object)

        self.depth -= 1
        return

    def dict_contains_only_attr(self, data):
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
