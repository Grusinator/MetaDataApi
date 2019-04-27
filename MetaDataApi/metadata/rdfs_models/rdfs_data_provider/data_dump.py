from MetaDataApi.metadata.models import ObjectInstance
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.rdfs_data_provider import RdfsDataProvider


class DataDump:

    def __init__(self, data_dump_pk):
        self.data_dump = ObjectInstance.objects.get(pk=data_dump_pk)

    @property
    def pk(self):
        return self.data_dump.pk

    @property
    def date_downloaded(self):
        return self.data_dump.get_att_inst_with_label(
            RdfsDataProvider.SchemaItems.date_downloaded.label
        ).value

    @property
    def file(self):
        return self.data_dump.get_att_inst_with_label(
            RdfsDataProvider.SchemaItems.data_dump_file.label
        ).value

    @property
    def loaded(self) -> bool:
        return self.data_dump.get_att_inst_with_label(
            RdfsDataProvider.SchemaItems.loaded.label
        ).value

    @loaded.setter
    def loaded(self, value: bool):
        loaded = self.data_dump.get_att_inst_with_label(
            RdfsDataProvider.SchemaItems.loaded.label
        )
        RdfsDataProvider.update_att_of_obj(loaded, value)

    @property
    def endpoint(self):
        from . import Endpoint
        endpoint = self.data_dump.get_parrent_obj_instances_with_relation(
            RdfsDataProvider.SchemaItems.has_generated.label
        )[0]
        return Endpoint(endpoint.pk)

    @classmethod
    def get_all_as_obj(cls, endpoint):
        data_dumps = RdfsDataProvider.get_all_data_dumps(endpoint)
        return [DataDump(data_dump.pk) for data_dump in data_dumps]
