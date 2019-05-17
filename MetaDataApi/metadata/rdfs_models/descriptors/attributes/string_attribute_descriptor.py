from MetaDataApi.metadata.models import StringAttributeInstance
from MetaDataApi.metadata.rdfs_models.descriptors.attributes.base_attribute_descriptor import BaseAttributeDescriptor


class StringAttributeDescriptor(BaseAttributeDescriptor):
    instance_type = StringAttributeInstance

    def __init__(self, has_many=False):
        super(StringAttributeDescriptor, self).__init__(self.instance_type, has_many)
