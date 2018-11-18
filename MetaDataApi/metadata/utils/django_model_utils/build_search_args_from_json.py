from ..json_utils import IJsonIterator


class BuildSearchArgsFromJson(IJsonIterator):
    base_arg_name = "from_relations__from_object__"

    def __init__(self):
        super(BuildSearchArgsFromJson, self).__init__()

        self.search_args = {}

    def add_arg(self, key, value):
        key_in = key + "__in"
        if key in self.search_args:
            old_val = self.search_args.pop(key)
            self.search_args[key_in] = [old_val, value]
        elif key_in in self.search_args:
            self.search_args[key_in].append(value)
        else:
            self.search_args[key] = value

    def handle_attributes(self, parrent_object, data, label):
        key = self.base_arg_name * self.depth + "label"
        self.add_arg(key, label)

    def handle_objects(self, parrent_object, data, label):
        key = self.base_arg_name * self.depth + "label"
        self.add_arg(key, label)

    def handle_object_relations(self, parrent_object, data, label):
        pass

    def build(self, data):
        self.iterate_json_tree(data)
        return self.search_args

    @staticmethod
    def modify_keys_in_dict(input_dict, func):
        return {func(key): value for key, value in input_dict.items()}
