from MetaDataApi.metadata.models import Attribute, BaseAttributeInstance
from MetaDataApi.metadata.rdfs_models.descriptors.base_descriptor import BaseDescriptor


class BaseAttributeDescriptor(BaseDescriptor):
    meta_type = Attribute

    def __init__(self, attribute_type: BaseAttributeInstance, has_many: bool = True):
        super(BaseAttributeDescriptor, self).__init__(self.meta_type)
        self.attribute_type = attribute_type
        self.label = None
        self.has_many = has_many

    def __get__(self, instance):
        if self.has_many:
            return self.get_attribute_values(instance)
        else:
            return self.get_attribute_value(instance)

    def __set__(self, instance, value):
        self.set_attributes(instance, value)

    def __delete__(self, instance):
        pass

    def get_attribute_value(self, instance):
        att_inst = instance.object_instance.get_att_inst_with_label(self.label)
        return att_inst.value if att_inst is not None else None

    def get_attribute_values(self, instance):
        return [att_inst.value for att_inst in instance.object_instance.get_all_att_insts_with_label(self.label)]

    def set_attributes(self, instance, values):
        att_instances = instance.object_instance.get_all_att_insts_with_label(self.label)
        att_inst_values = list(map(lambda x: x.value, att_instances))
        diff_elms = self.get_attribute_set_difference(values, att_inst_values)
        [instance.object_instance.create_att_inst(self.attribute_type, att_value) for att_value in diff_elms]

    @staticmethod
    def get_attribute_set_difference(list1, list2):
        if not isinstance(list1, (list, set, tuple)):
            list1 = [list1]
        return list(set(list1) - set(list2))
