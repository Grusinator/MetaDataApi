from MetaDataApi.metadata.models import BoolAttributeInstance
from MetaDataApi.metadata.rdfs_models.descriptors.attributes.base_attribute_descriptor import BaseAttributeDescriptor


class BoolAttributeDescriptor(BaseAttributeDescriptor):
    instance_type = BoolAttributeInstance

    def __init__(self, has_many=False):
        super(BoolAttributeDescriptor, self).__init__(self.instance_type, has_many)
