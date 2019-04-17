from MetaDataApi.metadata.models import ObjectInstance, Schema


class DataProviderO:
    def __init__(self, inst_pk):
        self.data_provider = ObjectInstance.objects.get(pk=inst_pk)

    @property
    def db_data_provider(self):
        return self.data_provider.db_data_provider.first()

    @property
    def schema(self):
        return Schema.objects.get(label=self.db_data_provider.provider_name)

    @property
    def endpoints(self):
        return []
