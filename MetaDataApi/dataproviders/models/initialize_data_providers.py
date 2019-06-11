import io
import logging

import boto3
from django.conf import settings

from MetaDataApi.dataproviders.models import DataProvider, Endpoint
from MetaDataApi.dataproviders.models.OauthConfig import OauthConfig
from MetaDataApi.metadata.utils import JsonUtils
from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils
from MetaDataApi.metadata.utils.json_utils.json_utils import JsonType

logger = logging.getLogger(__name__)


class InitializeDataProviders:
    local_client_file = "data_providers.json"

    @classmethod
    def load(cls):
        providers = cls.read_data_providers_from_file()
        [cls.try_create_provider(provider) for provider in providers]

    @classmethod
    def read_data_providers_from_file(cls):
        try:
            return JsonUtils.read_json_file(cls.local_client_file)
        except FileNotFoundError as e:
            return cls.get_providers_from_aws()

    @classmethod
    def try_create_provider(cls, provider: dict):
        try:
            cls.create_or_update_data_provider(provider)
        except Exception as e:
            logger.error(f'error durring loading of dataprovider {provider["provider_name"]} due to error {e}')

    @classmethod
    def create_or_update_data_provider(cls, provider_data: dict):
        provider_name = provider_data["provider_name"]
        data_provider = DataProvider.exists(provider_name)
        if data_provider:
            return cls.update_data_provider(data_provider, provider_data)
        else:
            return cls.create_data_provider(provider_data)

    @classmethod
    def update_data_provider(cls, data_provider, provider_data):
        endpoints_data, oauth_config = cls.split_into_data_objects(provider_data)
        DjangoModelUtils.update(data_provider, provider_data)
        DjangoModelUtils.update(data_provider.oauth_config, oauth_config)
        # TODO This approach has some flaws, if an endpoint is deleted etc.
        for endpoint, endpoint_data in zip(data_provider.endpoints.all(), endpoints_data):
            DjangoModelUtils.update(endpoint, endpoint_data)
        return data_provider

    @classmethod
    def create_data_provider(cls, provider_data: JsonType):
        endpoints_data, oauth_config = cls.split_into_data_objects(provider_data)
        data_provider = DataProvider.objects.create(**provider_data)
        OauthConfig.objects.create(data_provider=data_provider, **oauth_config)
        for endpoint in endpoints_data:
            Endpoint.objects.create(data_provider=data_provider, **endpoint)
        return data_provider

    @classmethod
    def split_into_data_objects(cls, provider_data):
        # TODO fix this
        remove_list = ["endpoints", "oauth_config", "http_config"]
        extracted_data = dict()
        extracted_data["endpoints"] = provider_data.pop("endpoints")
        extracted_data["oauth_config"] = provider_data.pop("oauth_config")
        extracted_data["oauth_config"]["scope"] = JsonUtils.dumps(extracted_data["oauth_config"]["scope"])
        return endpoints_data, oauth_config

    @classmethod
    def get_providers_from_aws(cls):
        path = "media/private/"
        file_name = path + "data_providers.json"
        return cls.read_file_from_aws(file_name)

    @classmethod
    def read_file_from_aws(cls, file_name: str):
        s3_resource = cls.get_aws_session()
        text = cls.read_aws_file(file_name, s3_resource)
        json_obj = JsonUtils.validate(text)
        return json_obj

    @classmethod
    def read_aws_file(cls, file_name, s3_resource):
        file = s3_resource.Object(settings.AWS_STORAGE_BUCKET_NAME, file_name)
        file_stream = io.BytesIO()
        file.download_fileobj(file_stream)
        string = file_stream.getvalue().decode("utf-8")
        return string

    @staticmethod
    def get_aws_session():
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        s3_resource = session.resource('s3')
        return s3_resource
