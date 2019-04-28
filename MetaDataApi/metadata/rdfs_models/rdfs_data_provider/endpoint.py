from django.urls import reverse

from MetaDataApi.metadata.models import ObjectInstance
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.base_rdfs_object import BaseRdfsObject
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.rdfs_data_provider import RdfsDataProvider
from .data_dump import DataDump
from .data_provider import DataProviderO

SI = RdfsDataProvider.SchemaItems


class Endpoint(BaseRdfsObject):
    MetaObject = SI.endpoint

    def __init__(self, inst_pk: int = None, json_object: dict = None):
        if not inst_pk:
            self.create_self(json_object)
        else:
            super(Endpoint, self).__init__(inst_pk)

    @property
    def name(self):
        return self.getAttribute(SI.endpoint_name)

    @name.setter
    def name(self, value):
        self.setAttribute(SI.endpoint_name, value)

    @property
    def url(self):
        return self.getAttribute(SI.endpoint_template_url)

    @url.setter
    def url(self, value):
        self.setAttribute(SI.endpoint_template_url, value)

    @property
    def data_dumps(self):
        data_dumps = self.getChildObjects(SI.has_generated)
        return [DataDump(data_dump.pk) for data_dump in data_dumps]

    @property
    def data_provider(self):
        data_provider = self.getParrentObjects(SI.provider_has_endpoint)[0]
        return DataProviderO(data_provider.pk)

    @property
    def api_type(self):
        return self.getAttribute(SI.api_type)

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
