from MetaDataApi.metadata.models import Schema
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.base_rdfs_object import BaseRdfsObject

from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType


class DataProviderO(BaseRdfsObject):
    from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.rdfs_data_provider import RdfsDataProvider
    SI = RdfsDataProvider.SchemaItems

    def __init__(self, inst_pk: int = None, db_data_provider=None):
        if inst_pk and db_data_provider:
            raise Exception("do not specify both DataProviderO")
        elif db_data_provider:
            db_data_provider.save()
            super(DataProviderO, self).__init__(db_data_provider.pk)
            self.db_data_provider_private = db_data_provider
            self.scope = db_data_provider.scope
            self.provider_name = db_data_provider.provider_name
            self.rest_endpoint_list = db_data_provider.rest_endpoints_list
        elif inst_pk:
            super(DataProviderO, self).__init__(inst_pk)
            self.db_data_provider_private = self.self_ref.db_data_provider.first()
        else:
            raise Exception("specify at least one DataProviderO")

    @property
    def db_data_provider(self):
        return self.db_data_provider_private

    @property
    def schema(self):
        return Schema.exists_by_label(self.db_data_provider.provider_name)

    @property
    def provider_name(self):
        return self.getAttribute(self.SI.data_provider_name)

    @provider_name.setter
    def provider_name(self, value: str):
        self.setAttribute(self.SI.data_provider_name, value)

    @property
    def api_endpoint(self):
        return self.db_data_provider_private.api_endpoint

    @property
    def authorize_url(self):
        return self.db_data_provider_private.authorize_url

    @property
    def access_token_url(self):
        return self.db_data_provider_private.access_token_url

    @property
    def client_id(self):
        return self.db_data_provider_private.client_id

    @property
    def client_secret(self):
        return self.db_data_provider_private.client_secret

    @property
    def scope(self):
        return self.getAttribute(self.SI.scope)

    @scope.setter
    def scope(self, value):
        self.setAttribute(self.SI.scope, value)

    @property
    def rest_endpoints_list(self):
        endpoints = self.getChildObjects(self.SI.provider_has_endpoint)

        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider import Endpoint
        return [Endpoint(endpoint.pk) for endpoint in endpoints]

    @rest_endpoints_list.setter
    def rest_endpoint_list(self, value: JsonType):
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider import Endpoint
        self.setChildObjects(self.SI.provider_has_endpoint, Endpoint, value)

    @property
    def json_schema_file_url(self):
        return ""

    @property
    def data_provider_instance(self):
        return self.self_ref
