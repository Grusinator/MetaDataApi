import io
import logging

import boto3
from django.conf import settings

from MetaDataApi.dataproviders.models import DataProvider
from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import DataProviderO
from MetaDataApi.metadata.utils import JsonUtils

logger = logging.getLogger(__name__)


class InitializeDataProviders:
    local_client_file = "data_providers.json"

    @classmethod
    def read_data_providers_from_file(cls):
        try:
            return JsonUtils.read_json_file(cls.local_client_file)
        except FileNotFoundError as e:
            return cls.get_providers_from_aws()

    @classmethod
    def load(cls):
        providers = cls.read_data_providers_from_file()
        [cls.try_create_provider(provider) for provider in providers]

    @classmethod
    def try_create_provider(cls, provider: dict):
        try:
            cls.create_if_does_not_exists(provider)
        except Exception as e:
            logger.error("error durring loading of dataprovider %s" % provider["provider_name"])

    @classmethod
    def create_if_does_not_exists(cls, provider_data: dict):
        provider_name = provider_data["provider_name"]
        data_provider = DataProvider.exists(provider_name)
        if data_provider is None:
            return DataProviderO(json_object=provider_data)
        else:
            pk = data_provider.data_provider_instance.pk
            return DataProviderO(inst_pk=pk, json_object=provider_data)

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
