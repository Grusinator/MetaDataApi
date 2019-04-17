from MetaDataApi.metadata.models import ObjectInstance, Schema
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.rdfs_data_provider import RdfsDataProvider


class DataProviderO:
    def __init__(self, inst_pk):
        self.data_provider = ObjectInstance.objects.get(pk=inst_pk)

    @property
    def schema(self):
        return Schema.exists(RdfsDataProvider.SchemaItems.schema)

    @property
    def endpoints(self):
        return []
