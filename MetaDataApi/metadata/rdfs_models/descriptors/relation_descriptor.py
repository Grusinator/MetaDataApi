import logging

from MetaDataApi.metadata.models import ObjectRelation, ObjectRelationInstance, ObjectInstance
from MetaDataApi.metadata.rdfs_models.descriptors.base_descriptor import BaseDescriptor
from MetaDataApi.metadata.rdfs_models.descriptors.object_list_singleton import RdfsModelInitializedList
from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType, JsonUtils

logger = logging.getLogger(__name__)


class ObjectRelationDescriptor(BaseDescriptor):
    meta_type = ObjectRelation

    def __init__(self, to_object, has_many: bool = True, parrent_relation=False):
        super(ObjectRelationDescriptor, self).__init__(self.meta_type)
        self.has_many = has_many
        self.parrent_relation = parrent_relation
        self.to_object = to_object

    def __get__(self, instance, obj_type=None):
        if self.parrent_relation:
            return self.get_parrent_objects(instance)
        else:
            return self.get_child_objects(instance)

    def __set__(self, instance, value):
        if self.parrent_relation:
            raise Exception("cannot set parrent, only child")
        else:
            self.set_child_objects(instance, value)

    def __delete__(self, instance):
        pass

    @property
    def rdfs_model(self):
        if isinstance(self.to_object, str):
            return RdfsModelInitializedList.get_by_name(self.to_object)
        else:
            RdfsModelInitializedList.set(self.to_object)
        return self.to_object

    def get_parrent_objects(self, instance):
        return instance.object_instance.get_parrent_obj_instances_with_relation(self.label)

    def get_child_objects(self, instance):
        return instance.object_instance.get_child_obj_instances_with_relation(self.label)

    def set_child_objects(self, instance, value: JsonType):
        existing_as_json_set = self.existing_objects_as_json_set(instance.object_instance)
        new_as_json_set = self.value_to_json(value)
        diff_elms = new_as_json_set - existing_as_json_set
        # RdfsObjectType is a class type used to instantiate the related object assuming that all dict keys match
        # the arguments
        child_objects = [self.create_child_object(child) for child in diff_elms]
        self.create_relations(child_objects, instance.object_instance)

    def create_child_object(self, child):
        RdfsObjectType = self.rdfs_model
        return RdfsObjectType(json_object=JsonUtils.validate(child))

    def create_relations(self, child_objects, object_instance):
        for child_object in child_objects:
            self.create_obj_rel_inst(self.label, object_instance, child_object.object_instance)

    @classmethod
    def create_obj_rel_inst(cls, obj_rel_label, from_object: ObjectInstance, to_object: ObjectInstance):
        rel_base = ObjectRelation.exists_by_label(
            obj_rel_label,
            from_object.base.label,
            to_object.base.label,
            from_object.base.schema.label
        )
        rel = ObjectRelationInstance(
            base=rel_base,
            from_object=from_object,
            to_object=to_object
        )
        rel.save()
        return rel

    def value_to_json(self, value: JsonType):
        if isinstance(value, list):
            return {JsonUtils.dumps(val) for val in value}
        elif isinstance(value, dict):
            return set(JsonUtils.dumps(value))

    def existing_objects_as_json_set(self, object_instance):
        obj_instances = object_instance.get_child_obj_instances_with_relation(self.label)
        existing_rdf_obj = [self.rdfs_model(obj_inst.pk) for obj_inst in obj_instances]
        return {obj.to_json() for obj in existing_rdf_obj}