from MetaDataApi.metadata.rdfs_models.base_rdfs_object import BaseRdfsModel
from MetaDataApi.metadata.rdfs_models.descriptors import *


class DataDump(BaseRdfsModel):
    def __init__(self, inst_pk):
        super(DataDump, self).__init__(inst_pk=inst_pk)

    date_downloaded = DateTimeAttributeDescriptor()
    file = FileAttributeDescriptor()
    loaded = BoolAttributeDescriptor()
    file_origin_url = StringAttributeDescriptor()
    has_data_dump = ObjectRelationDescriptor("Endpoint", parrent_relation=True)
