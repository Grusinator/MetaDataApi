from urllib import parse

from django.conf import settings

from MetaDataApi.metadata.models import Schema
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.base_rdfs_object import BaseRdfsObject
from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType


class DataProviderO(BaseRdfsObject):
    from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.rdfs_data_provider import RdfsDataProvider
    SI = RdfsDataProvider.SchemaItems
    MetaObject = SI.data_provider

    def __init__(self, inst_pk: int = None, json_object: dict = dict()):
        if inst_pk is None:
            self.create_data_provider_with_db_obj(json_object)
        else:
            super(DataProviderO, self).__init__(inst_pk)
            self._db_data_provider = self.get_db_data_provider_from_obj_inst()
            self.update_from_json(json_object)

    def get_db_data_provider_from_obj_inst(self):
        from MetaDataApi.dataproviders.models import DataProvider
        return DataProvider.objects.get(data_provider_instance=self.object_instance)

    def create_data_provider_with_db_obj(self, json_object):
        self.create_db_data_provider(json_object)
        self.create_self(json_object)

    def create_db_data_provider(self, json_object):
        from MetaDataApi.dataproviders.models import DataProvider
        db_params = self.filter_db_provider_params(json_object)
        self._db_data_provider = DataProvider(**db_params)
        self._db_data_provider.save()

    @staticmethod
    def filter_db_provider_params(json_object):
        keys = ["provider_name", "client_id", "client_secret", ]
        return {k: v for k, v in json_object.items() if k in keys}

    @property
    def db_data_provider(self):
        return self._db_data_provider

    @property
    def schema(self):
        return Schema.exists_by_label(self.db_data_provider.provider_name)

    @property
    def provider_name(self):
        return self.get_attribute_value(self.SI.data_provider_name)

    @provider_name.setter
    def provider_name(self, value: str):
        self.setAttribute(self.SI.data_provider_name, value)

    @property
    def endpoint_template_url(self):
        return self.get_attribute_value(self.SI.endpoint_url)

    @endpoint_template_url.setter
    def endpoint_template_url(self, value: str):
        self.setAttribute(self.SI.endpoint_url, value)

    @property
    def authorize_url(self):
        return self.get_attribute_value(self.SI.authorize_url)

    @authorize_url.setter
    def authorize_url(self, value: str):
        self.setAttribute(self.SI.authorize_url, value)

    @property
    def access_token_url(self):
        return self.get_attribute_value(self.SI.access_token_url)

    @access_token_url.setter
    def access_token_url(self, value: str):
        self.setAttribute(self.SI.access_token_url, value)

    @property
    def api_type(self):
        return self.get_attribute_value(self.SI.api_type)

    @api_type.setter
    def api_type(self, value: str):
        self.setAttribute(self.SI.api_type, value)

    @property
    def client_id(self):
        return self._db_data_provider.client_id

    @client_id.setter
    def client_id(self, value: str):
        self._db_data_provider.client_id = value
        self._db_data_provider.save()

    @property
    def client_secret(self):
        return self._db_data_provider.client_secret

    @client_secret.setter
    def client_secret(self, value: str):
        self._db_data_provider.client_secret = value
        self._db_data_provider.save()

    @property
    def scope(self):
        return self.get_attribute_values(self.SI.scope)

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
        return self.object_instance

    def build_auth_url(self, logged_in_user_id=None):

        state = "%s:%s" % (self.provider_name,
                           logged_in_user_id or "AnonomousUser")

        try:
            # TODO the set method is a quickfix. the scopes are created multiple times. look at how atts are set
            scopes = set(self.scope)
            scopes = " ".join(scopes)

        except:
            scopes = ""

        args = {
            "client_id": self.client_id,
            "redirect_uri": settings.OAUTH_REDIRECT_URI,
            "scope": scopes,
            "nounce": "sdfkjlhasdfdhfas",
            "response_type": "code",
            "response_mode": "form_post",
            "state": state,
        }
        if args["scope"] == "" or None:
            args.pop("scope")

        args_string = parse.urlencode(tuple(args.items()))

        url = "%s?%s" % (self.authorize_url, args_string)

        return url
