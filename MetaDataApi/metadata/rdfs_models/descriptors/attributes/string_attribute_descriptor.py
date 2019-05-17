from MetaDataApi.metadata.models import StringAttributeInstance
from MetaDataApi.metadata.rdfs_models.descriptors.attributes.base_attribute_descriptor import BaseAttributeDescriptor


class StringAttributeDescriptor(BaseAttributeDescriptor):
    instance_type = StringAttributeInstance

    def __init__(self, has_many=False):
        super(StringAttributeDescriptor, self).__init__(self.instance_type, has_many)

    # def __get__(self, instance):
    #     super(StringAttributeDescriptor, self).__get__(instance)
    #
    # def __set__(self, instance, value):
    #     super(StringAttributeDescriptor, self).__set__(instance, value)
    #
    # def __delete__(self, instance):
    #     super(StringAttributeDescriptor, self).__delete__(instance)
