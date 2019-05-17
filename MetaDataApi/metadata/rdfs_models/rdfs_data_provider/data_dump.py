from MetaDataApi.metadata.models import ObjectInstance
from MetaDataApi.metadata.rdfs_models.descriptors import *



class DataDump:
    def __init__(self, data_dump_pk):
        self.data_dump = ObjectInstance.objects.get(pk=data_dump_pk)

    date_downloaded = DateTimeAttributeDescriptor()
    file = FileAttributeDescriptor()
    loaded = BoolAttributeDescriptor()
    file_origin_url = StringAttributeDescriptor()
    has_endpoint = ObjectRelationDescriptor("Endpoint", parrent_relation=True)
