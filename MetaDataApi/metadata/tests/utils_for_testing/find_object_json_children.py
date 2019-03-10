from metadata.models import Schema, Object, ObjectInstance
from metadata.utils import json_utils


class FindObjectJsonChildren(json_utils.IJsonIterator):
    base_arg_name = "from_relations__from_object__"

    def __init__(self, schema: str):
        super(FindObjectJsonChildren, self).__init__()
        self.schema = Schema.objects.get(label=schema)

        self.childrens = []

    def handle_attributes(self, parrent_object, data, label):
        pass

    def handle_objects(self, parrent_object, data, label):
        try:
            obj = Object.objects.get(schema=self.schema, label=label)
            obj_inst = ObjectInstance(base=obj)
            self.childrens.append((obj_inst, data))
        except:
            teat = 1

    def handle_object_relations(self, parrent_object, data, label):
        pass

    def build_from_json(self, data):
        self.iterate_json_tree(data)
        return self.childrens
