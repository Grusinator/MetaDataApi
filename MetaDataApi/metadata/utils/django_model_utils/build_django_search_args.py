from MetaDataApi.metadata.utils.json_utils import IJsonIterator


class BuildDjangoSearchArgs(IJsonIterator):
    from_obj_rel_search_str = "from_edge__from_object__"
    to_obj_rel_search_str = "to_edge__to_object__"

    def __init__(self):
        super(BuildDjangoSearchArgs, self).__init__()

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
        key = self.from_obj_rel_search_str * self.depth + "label"
        self.add_arg(key, label)

    def handle_objects(self, parrent_object, data, label):
        key = self.from_obj_rel_search_str * self.depth + "label"
        self.add_arg(key, label)

    def handle_schema_edges(self, parrent_object, data, label):
        pass

    def build_from_json(self, data):
        self.iterate_json_tree(data)
        return self.search_args

    def add_from_obj(self, label, depth=1):
        self._add_obj(label, depth, to=False)

    def add_to_obj(self, label, depth=1):
        self._add_obj(label, depth, to=True)

    def _add_obj(self, label, depth, to=True):
        obj_str = self.to_obj_rel_search_str if to else self.from_obj_rel_search_str
        key = obj_str * depth
        # if it is a string assume its a label, else its an object
        if isinstance(label, str):
            key += "label"
        else:
            key = key[:-2]
        self.add_arg(key, label)

    @staticmethod
    def modify_keys_in_dict(input_dict, func):
        return {func(key): value for key, value in input_dict.items()}
