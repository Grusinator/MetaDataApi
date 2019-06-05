from urllib import parse

from django.conf import settings

from MetaDataApi.metadata.models import Schema
from MetaDataApi.metadata.rdfs_models.base_rdfs_object import BaseRdfsModel
from MetaDataApi.metadata.rdfs_models.descriptors.attributes.string_attribute_descriptor import \
    StringAttributeDescriptor
from MetaDataApi.metadata.rdfs_models.descriptors.relation_descriptor import ObjectRelationDescriptor
from MetaDataApi.metadata.utils.common_utils import StringUtils


class GrpDataProvider(BaseRdfsModel):
    data_provider_name = StringAttributeDescriptor()
    api_endpoint = StringAttributeDescriptor()
    scope = StringAttributeDescriptor(has_many=True)
    api_type = StringAttributeDescriptor()
    authorize_url = StringAttributeDescriptor()
    client_id = StringAttributeDescriptor()
    client_secret = StringAttributeDescriptor()
    access_token_url = StringAttributeDescriptor()

    from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.endpoint import Endpoint
    endpoints = ObjectRelationDescriptor(Endpoint, has_many=True)

    def __init__(self, inst_pk: int = None, json_object: dict = dict()):
        if inst_pk is None:
            self.create_data_provider_with_db_obj(json_object)
        else:
            super(GrpDataProvider, self).__init__(inst_pk)
            self._db_data_provider = self.get_db_data_provider_from_obj_inst()

            self.update_from_json(json_object)

    def get_db_data_provider_from_obj_inst(self):
        from MetaDataApi.dataproviders.models import DataProvider
        return DataProvider.objects.get(data_provider_instance=self.object_instance)

    def create_data_provider_with_db_obj(self, json_object):
        # self.create_db_data_provider(json_object)
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
    def data_provider_instance(self):
        return self.object_instance

    def build_auth_url(self, logged_in_user_id=None):

        state = "%s:%s" % (self.data_provider_name,
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

    def validate(self):
        valid = not StringUtils.is_string_none(self.api_endpoint) and \
                not StringUtils.is_string_none(self.access_token_url)

        if not valid:
            raise Exception("data provider validation error")
