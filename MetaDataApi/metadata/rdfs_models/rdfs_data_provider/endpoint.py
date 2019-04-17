from django.urls import reverse

from MetaDataApi.metadata.models import ObjectInstance
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.rdfs_data_provider import RdfsDataProvider
from .data_dump import DataDump
from .data_provider import DataProviderO


class Endpoint:
    def __init__(self, inst_pk):
        self.endpoint = ObjectInstance.objects.get(pk=inst_pk)

    @property
    def name(self):
        name_att = self.endpoint.get_att_inst(RdfsDataProvider.SchemaItems.endpoint_name.label)
        return name_att.value

    @property
    def url(self):
        url_att = self.endpoint.get_att_inst(RdfsDataProvider.SchemaItems.endpoint_template_url.label)
        return url_att.value

    @property
    def data_dumps(self):
        data_dumps = self.endpoint.get_child_obj_instance_with_relation(
            RdfsDataProvider.SchemaItems.has_generated.label
        )
        return [DataDump(data_dump) for data_dump in data_dumps]

    @property
    def data_provider(self):
        data_provider = self.endpoint.get_parrent_obj_instance_with_relation(
            RdfsDataProvider.SchemaItems.has_rest_endpoint.label
        )
        return DataProviderO(data_provider[0].pk)

    @classmethod
    def get_all_endpoints_as_objects(cls, provider: ObjectInstance):
        endpoints = RdfsDataProvider.get_all_endpoints(provider)
        return [Endpoint(endpoint.pk) for endpoint in endpoints]

    @classmethod
    def get_endpoint_as_object(cls, provider: ObjectInstance, endpoint_name: str):
        endpoint = RdfsDataProvider.get_endpoint(provider, endpoint_name)
        return Endpoint(endpoint.pk)

    def get_internal_view_url(self):
        schema = self.data_provider.schema
        return reverse('endpoint_detail', args=[str(schema.label), self.name])
