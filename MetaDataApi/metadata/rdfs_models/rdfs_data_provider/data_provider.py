
from MetaDataApi.metadata.models import Schema
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.base_rdfs_object import BaseRdfsObject

from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType


class DataProviderO(BaseRdfsObject):
    from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.rdfs_data_provider import RdfsDataProvider
    SI = RdfsDataProvider.SchemaItems
    MetaObject = SI.data_provider

    def __init__(self, inst_pk: int = None, json_object: dict = None):
        if not inst_pk:
            from MetaDataApi.dataproviders.models import DataProvider
            self.db_data_provider_private = DataProvider(**json_object)
            self.db_data_provider_private.save()
            json_object["endpoints"] = json_object.pop("rest_endpoints_list")

            self.create_self(json_object)
        else:
            super(DataProviderO, self).__init__(inst_pk)
            self.db_data_provider_private = self.self_ref.db_data_provider.first()

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
        return self.getAttributes(self.SI.scope)

    @scope.setter
    def scope(self, value):
        self.setAttribute(self.SI.scope, value)

    @property
    def endpoints(self):
        endpoints = self.getChildObjects(self.SI.provider_has_endpoint)

        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider import Endpoint
        return [Endpoint(endpoint.pk) for endpoint in endpoints]

    @endpoints.setter
    def endpoints(self, value: JsonType):
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider import Endpoint
        self.setChildObjects(self.SI.provider_has_endpoint, Endpoint, value)

    @property
    def json_schema_file_url(self):
        return ""

    @property
    def data_provider_instance(self):
        return self.self_ref
