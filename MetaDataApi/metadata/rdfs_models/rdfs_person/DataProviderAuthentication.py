from MetaDataApi.metadata.rdfs_models.base_rdfs_object import BaseRdfsModel
from MetaDataApi.metadata.rdfs_models.descriptors import StringAttributeDescriptor, ObjectRelationDescriptor
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import GrpDataProvider
from MetaDataApi.metadata.rdfs_models.rdfs_person.Person import Person


class DataProviderAuthentication(BaseRdfsModel):
    name = StringAttributeDescriptor()
    person = ObjectRelationDescriptor(Person, parrent_relation=True)
    data_provider = ObjectRelationDescriptor(GrpDataProvider)
    auth_token = StringAttributeDescriptor()
