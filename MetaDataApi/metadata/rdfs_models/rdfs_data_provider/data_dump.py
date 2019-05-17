from MetaDataApi.metadata.models import ObjectInstance
from MetaDataApi.metadata.rdfs_models.descriptors import *



class DataDump:
    def __init__(self, data_dump_pk):
        self.data_dump = ObjectInstance.objects.get(pk=data_dump_pk)

    date_downloaded = DateTimeAttributeDescriptor()
    file = FileAttributeDescriptor()
    loaded = BoolAttributeDescriptor()
    # from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.endpoint import Endpoint
    has_endpoint = ObjectRelationDescriptor(None, parrent_relation=True)
