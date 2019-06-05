from MetaDataApi.metadata.rdfs_models.base_rdfs_object import BaseRdfsModel
from MetaDataApi.metadata.rdfs_models.descriptors import StringAttributeDescriptor


class Person(BaseRdfsModel):
    name = StringAttributeDescriptor()
