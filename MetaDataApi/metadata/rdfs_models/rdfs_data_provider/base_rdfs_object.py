import logging

from MetaDataApi.metadata.models import ObjectInstance, Attribute, ObjectRelation
from MetaDataApi.metadata.rdfs_models.base_rdfs_model import BaseRdfsModel
from MetaDataApi.metadata.utils import JsonUtils
from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType

logger = logging.getLogger(__name__)

class BaseRdfsObject:
    MetaObject = None

    def __init__(self, inst_pk):
        self.self_ref = ObjectInstance.objects.get(pk=inst_pk)

    def create_self(self, json_object: dict):
        self.self_ref = ObjectInstance(base=self.MetaObject)
        self.self_ref.save()
        for key, value in json_object.items():
            try:
                setattr(self, key, value)
            except Exception as e:
                logger.warning("could not set key: %s " %key)
                pass

    def getAttribute(self, att: Attribute):
        return self.self_ref.get_att_inst_with_label(att.label)

    def getAttributes(self, att: Attribute) -> list:
        return self.self_ref.get_all_att_insts_with_label(att.label)

    def setAttribute(self, att: Attribute, value):
        att_instances = self.self_ref.get_all_att_insts_with_label(att.label)
        diff_elms = self.get_attribute_set_diffence(value, att_instances)
        [self.self_ref.create_att_inst(att, att_value) for att_value in diff_elms]

    def getParrentObjects(self, rel: ObjectRelation):
        return self.self_ref.get_parrent_obj_instances_with_relation(rel.label)

    def getChildObjects(self, rel: ObjectRelation):
        return self.self_ref.get_child_obj_instances_with_relation(rel.label)

    def setChildObjects(self, rel: ObjectRelation, RdfsObjectType: type, value: JsonType):

        obj_instances = self.self_ref.get_child_obj_instances_with_relation(rel.label)
        diff_elms = self.get_json_set_diffence(value, obj_instances)

        # RdfsObjectType is a class type used to instantiate the related object assuming that all dict keys match
        # the arguments
        endpoints = [RdfsObjectType(json_object=diff) for diff in diff_elms]
        [BaseRdfsModel.create_obj_rel_inst(rel, self.self_ref, endpoint.self_ref) for endpoint in endpoints]




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
