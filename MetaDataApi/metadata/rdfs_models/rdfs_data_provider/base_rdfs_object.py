import logging

from MetaDataApi.metadata.models import ObjectInstance, Attribute, ObjectRelation, Object
from MetaDataApi.metadata.rdfs_models.base_rdfs_model import BaseRdfsModel
from MetaDataApi.metadata.utils import JsonUtils
from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType

logger = logging.getLogger(__name__)


class BaseRdfsObject:
    SI = None
    MetaObject = None

    def __init__(self, inst_pk):
        self.object_instance = ObjectInstance.objects.get(pk=inst_pk)

    # TODO this breaks debugging
    # def __getattribute__(self, name):
    #     att = getattr(self.SI, name)
    #     return self.getAttribute(att)
    #
    #     # raise Exception("not a valid attribute")
    #     # return super(BaseRdfsObject, self).__getattribute__(name)

    # def __setattr__(self, name, value):
    #     if hasattr(self.SI, name):
    #         att = getattr(self.SI, name)
    #         self.setAttribute(att, value)
    #     else:
    #         return super(BaseRdfsObject, self).__setattr__(name, value)

    def get_base_object(self):
        return Object.exists(self.MetaObject)

    def create_self(self, json_object: dict):
        self.object_instance = ObjectInstance(base=self.get_base_object())
        self.object_instance.save()
        self.update_from_json(json_object)

    def update_from_json(self, json_object):
        if json_object is not None:
            for key, value in json_object.items():
                try:
                    setattr(self, key, value)
                except Exception as e:
                    logger.warning("could not set key: %s  with value: %s ____ exc: %s" % (key, value, e))
                    pass

    def getAttribute(self, att: Attribute):
        return self.object_instance.get_att_inst_with_label(att.label)

    def get_attribute_value(self, att: Attribute):
        return self.getAttribute(att).value

    def getAttributes(self, att: Attribute) -> list:
        return self.object_instance.get_all_att_insts_with_label(att.label)

    def get_attribute_values(self, att: Attribute):
        return [att_inst.value for att_inst in self.getAttributes(att)]

    def setAttribute(self, att: Attribute, value):
        att_instances = self.object_instance.get_all_att_insts_with_label(att.label)
        diff_elms = self.get_attribute_set_diffence(value, att_instances)
        [self.object_instance.create_att_inst(att, att_value) for att_value in diff_elms]

    def getParrentObjects(self, rel: ObjectRelation):
        return self.object_instance.get_parrent_obj_instances_with_relation(rel.label)

    def getChildObjects(self, rel: ObjectRelation):
        return self.object_instance.get_child_obj_instances_with_relation(rel.label)

    def setChildObjects(self, rel: ObjectRelation, RdfsObjectType: type, value: JsonType):
        existing_as_json_set = self.existing_objects_as_json_set(RdfsObjectType, rel)
        new_as_json_set = self.value_to_json(value)
        diff_elms = new_as_json_set - existing_as_json_set
        # RdfsObjectType is a class type used to instantiate the related object assuming that all dict keys match
        # the arguments
        child_objects = [RdfsObjectType(json_object=JsonUtils.validate(diff)) for diff in diff_elms]
        self.create_relations(child_objects, rel)

    def value_to_json(self, value: JsonType):
        if isinstance(value, list):
            return {JsonUtils.dumps(val) for val in value}
        elif isinstance(value, dict):
            return set(JsonUtils.dumps(value))

    def existing_objects_as_json_set(self, RdfsObjectType, rel):
        obj_instances = self.object_instance.get_child_obj_instances_with_relation(rel.label)
        existing_rdf_obj = [RdfsObjectType(obj_inst.pk) for obj_inst in obj_instances]
        return {obj.to_json() for obj in existing_rdf_obj}


    def create_relations(self, child_objects, rel):
        for child_object in child_objects:
            BaseRdfsModel.create_obj_rel_inst(rel, self.object_instance, child_object.object_instance)

    @staticmethod
    def get_json_set_diffence(list1: JsonType, list2: JsonType):
        if len(list2) is 0:
            return list1

        list1 = JsonUtils.to_tuple_set_key_value(list1)
        list2 = JsonUtils.to_tuple_set_key_value(list2)

        diff_elms = set(list1) - set(list2)
        return diff_elms

    @staticmethod
    def get_attribute_set_diffence(list1, list2):
        if not isinstance(list1, (list, set, tuple)):
            list1 = [list1]
        return set(list1) - set(list2)

    def build_json_from_att_names(self, att_names: list) -> str:
        return JsonUtils.dumps({att_name: getattr(self, att_name) for att_name in att_names})
