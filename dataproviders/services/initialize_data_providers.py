import io
import logging
import os

import boto3
from django.conf import settings
from generic_serializer import SerializableModelFilter

from MetaDataApi.utils import JsonUtils
from dataproviders.models import DataProvider
from dataproviders.serializers.DataProviderSerializer import DataProviderSerializer

logger = logging.getLogger(__name__)


class InitializeDataProviders:
    data_providers_filename = "data_providers.json"
    exclude = (
        "dataprovideruser",
        "data_fetch",
        "data_fetches",
        # "endpoints",
        # "oauth_config",
        # "http_config"
    )

    model_filter = SerializableModelFilter(
        exclude_labels=exclude,
        max_depth=4,
        start_object_name="data_provider"
    )

    @classmethod
    def load(cls):
        providers = cls.get_data_providers_from_local_or_remote_file()
        [cls.try_create_provider(provider) for provider in providers]

    @classmethod
    def get_data_providers_from_local_or_remote_file(cls):
        try:
            return JsonUtils.read_json_file(cls.data_providers_filename)
        except FileNotFoundError as e:
            return cls.get_providers_from_aws()
        except Exception as e:
            logger.error(f"another error than fileNotFound has occured Msg: {e}")
            return cls.get_providers_from_aws()

    @classmethod
    def try_create_provider(cls, provider_data: dict):
        try:
            cls.create_data_provider(provider_data)
        except Exception as e:
            logger.error(f'error durring loading of dataprovider {provider_data["provider_name"]} due to error {e}')

    @classmethod
    def update_data_provider_to_json_file(cls, data_provider: DataProvider):
        serialized_dp = data_provider.serialize(
            filter=cls.model_filter)  # TODO test this properly, the serialization is not correct
        data = InitializeDataProviders.read_data_from_data_provider_json_file(fail_on_file_missing=False)
        index, provider = InitializeDataProviders.find_provider_with_name(data, data_provider)
        # TODO serialize by id instead
        if index is not None:
            data[index] = serialized_dp
        else:
            data.append(serialized_dp)
        cls.write_data_to_json_file(data)

    @classmethod
    def find_provider_with_name(cls, data: list, data_provider: DataProvider):
        for i, provider in enumerate(data):
            if provider["provider_name"] == data_provider.provider_name:
                return i, provider
        return None, None

    @classmethod
    def create_empty_provider_file(cls):
        with open(cls.data_providers_filename, "w+") as provider_file:
            provider_file.write("[]")

    @classmethod
    def read_data_from_data_provider_json_file(cls, fail_on_file_missing=True):
        try:
            data = open(cls.data_providers_filename).read()
        except FileNotFoundError as e:
            cls.create_empty_provider_file()
            if fail_on_file_missing:
                raise e
            else:
                return []
        else:
            if not data and fail_on_file_missing:
                raise FileNotFoundError("there is no providers in the file")
            else:
                return JsonUtils.validate(data or [])

    @classmethod
    def write_data_to_json_file(cls, data):
        with open(cls.data_providers_filename, 'w+') as data_providers_file:
            data_providers_file.write(JsonUtils.dumps(data))

    @classmethod
    def create_data_provider(cls, provider_data):
        provider_name = provider_data["provider_name"]
        data_provider = DataProvider.exists(provider_name)
        if data_provider:
            data_provider.delete()
            logger.debug("provider exists - deleted")
        data_provider = cls.deserialize_data_provider(provider_data)
        logger.debug(f"provider saved: {provider_name}")
        return data_provider

    @classmethod
    def deserialize_data_provider(cls, provider_data):
        serializer = DataProviderSerializer(data=provider_data)
        if serializer.is_valid():
            return serializer.save()
        else:
            raise ValueError(serializer.errors)

    @classmethod
    def deserialize_data_provider_generic(cls, provider_data):
        return DataProvider.deserialize(
            provider_data,
            filter=SerializableModelFilter(
                exclude_labels=cls.exclude,
                max_depth=4,
                start_object_name="data_provider"
            )
        )

    @classmethod
    def get_providers_from_aws(cls):
        file_name = os.path.join(settings.PRIVATE_MEDIA_LOCATION, cls.data_providers_filename).replace("\\", "/")
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
