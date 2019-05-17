from MetaDataApi.metadata.models import DateTimeAttributeInstance
from MetaDataApi.metadata.rdfs_models.descriptors.attributes.base_attribute_descriptor import BaseAttributeDescriptor


class DateTimeAttributeDescriptor(BaseAttributeDescriptor):
    instance_type = DateTimeAttributeInstance

    def __init__(self, has_many=False):
        super(DateTimeAttributeDescriptor, self).__init__(self.instance_type, has_many)
