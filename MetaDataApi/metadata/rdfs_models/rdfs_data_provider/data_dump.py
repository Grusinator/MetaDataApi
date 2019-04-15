from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.rdfs_data_provider import RdfsDataProvider


class DataDump:

    def __init__(self, data_dump):
        self.data_dump = data_dump

    @property
    def date_downloaded(self):
        return self.data_dump.get_att_inst(RdfsDataProvider.SchemaItems.date_downloaded.label).value

    @property
    def file(self):
        return self.data_dump.get_att_inst(RdfsDataProvider.SchemaItems.data_dump_file.label).value

    @classmethod
    def get_all_data_dumps_as_obj(cls, endpoint):
        data_dumps = RdfsDataProvider.get_all_data_dumps(endpoint)
        return [DataDump(data_dump.pk) for data_dump in data_dumps]
