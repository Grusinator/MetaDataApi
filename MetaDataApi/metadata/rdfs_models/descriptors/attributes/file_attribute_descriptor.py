from MetaDataApi.metadata.models import FileAttributeInstance
from MetaDataApi.metadata.rdfs_models.descriptors.attributes.base_attribute_descriptor import BaseAttributeDescriptor


class FileAttributeDescriptor(BaseAttributeDescriptor):
    instance_type = FileAttributeInstance

    def __init__(self, has_many=False):
        super(FileAttributeDescriptor, self).__init__(self.instance_type, has_many)
