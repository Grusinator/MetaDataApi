from .json_utils import IJsonIterator


class DjangoModelUtils:

    class BuildSearchArgsFromJson(IJsonIterator):
        base_arg_name = "from_relations__from_object__"

        def __init__(self, *args, **kwargs):
            super(BuildSearchArgsFromJson, self).__init__(
                self, *args, **kwargs)

            self.search_args = {}

        def handle_attributes(self, parrent_object, data, label):
            key = self.base_arg_name * self.depth
            self.search_args[key] = label

        def handle_objects(self, parrent_object, data, label):
            key = self.base_arg_name * self.depth
            self.search_args[key] = label

        def handle_object_relations(self, parrent_object, data, label):
            pass

        def build_search_args_from_json(self, data):
            self.iterate_json_tree(data)
            return self.search_args

        @classmethod
        def build_search_args_from_json_dummy(cls, json_childrens):
            search_args = {}
            base_arg_name = "from_relations__from_object__"
            arg_name = ""
            # loop though all but last
            for obj in path:
                if isinstance(obj, Attribute):
                    arg_name += "object__"
                    search_args["base__label"] = obj.label
                elif obj == obj_inst.base:
                    # last elm add primary key
                    search_args[arg_name + "pk"] = obj_inst.pk
                else:
                    # Not neccesary as long as pk is being added
                    # search_args[arg_name + "base__label"] = obj.label
                    arg_name += base_arg_name

            return search_args
            pass
