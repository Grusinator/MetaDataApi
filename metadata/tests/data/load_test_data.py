import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from generic_serializer import SerializableModelFilter

from MetaDataApi.utils import JsonUtils
from dataproviders.models import DataProvider, Endpoint
from dataproviders.models import DataProviderUser
from metadata.models import Schema, SchemaEdge, SchemaNode, SchemaAttribute
from metadata.services import (
    JsonSchemaService, DataCleaningService, RdfInstanceService, RdfSchemaService, JsonAnalyser
)
from users.models import Profile


class LoadTestData:

    @staticmethod
    def init_user():

        user = User(
            username="test",
            password="test1234"
        )
        try:
            user = User.objects.get(username=user.username)
        except:
            user.save()

        return user

    @staticmethod
    def init_profile(user):
        LoadTestData.init_foaf()
        profile = Profile(
            user=user,
        )
        try:
            return Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            profile.save()
        return profile

    @classmethod
    def init_foaf_person(cls):
        schema = cls.init_foaf()
        return SchemaNode.objects.get(label="person", schema=schema)

    @staticmethod
    def init_foaf():

        rdf_service = RdfSchemaService()
        # just take foaf
        rdf_service.write_to_db(rdf_url="http://xmlns.com/foaf/0.1/")

        return rdf_service.schema

    @staticmethod
    def init_strava_data_provider_profile() -> DataProviderUser:
        LoadTestData.init_foaf()
        user = LoadTestData.init_user()
        LoadTestData.init_profile(user)

        provider = DataProvider.objects.filter(provider_name="strava").first()

        assert provider, "Remember to init DataProviders before loading provider profile"

        Endpoint.objects.create(
            data_provider=provider,
            endpoint_name="activity",
            endpoint_url="v3/activities"
        )

        return DataProviderUser.objects.create(
            data_provider=provider,
            access_token="174323610143cdcd159f7792c1c4ec5637a96e12",
            user=user
        )

    @staticmethod
    def init_meta_data_api():
        rdf_service = RdfSchemaService()
        rdf_service.write_to_db(
            rdf_url="https://meta-data-api-storage-dev.s3.amazonaws.com/media/schemas/meta_data_api.ttl"
        )

        # TODO fix error in obj rel load, this is a temp fix
        schema = Schema.objects.get(label="meta_data_api")
        data_fetch = SchemaNode.objects.get(schema=schema, label="endpoint_data_fetch")
        SchemaEdge(
            schema=schema,
            label="has_generated",
            from_object=SchemaNode.objects.get(schema=schema, label="rest_endpoint"),
            to_object=data_fetch
        ).save()

        att = SchemaAttribute.objects.get(label="data_fetch_file", object=data_fetch)
        att.data_type = "file"
        att.save()

        return rdf_service.schema

    @staticmethod
    def init_strava_schema_from_file():

        LoadTestData.init_foaf()

        rdf_inst = RdfInstanceService()

        data_cleaning = DataCleaningService()

        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        data = JsonUtils.read_json_file(testfile)

        service = JsonAnalyser()

        schema_label = "strava"
        label = "activities"

        schema = Schema.create_new_empty_schema(schema_label)

        user = LoadTestData.init_user()
        LoadTestData.init_profile(user)

        service.identify_from_json_data(
            data, schema, user, parrent_label=label)
        data_cleaning.relate_root_classes_to_foaf(schema)

        return schema

    @staticmethod
    def init_strava_data_from_file():
        user = LoadTestData.init_user()
        LoadTestData.init_profile(user)

        service = JsonAnalyser()

        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        data = JsonUtils.read_json_file(testfile)

        schema = Schema.objects.get(label="strava")

        label = "activities"

        objects = service.identify_from_json_data(
            data, schema, parrent_label=label, owner=user)

        return objects

    @staticmethod
    def init_open_m_health_sample(extras=None):

        schema_label = "open_m_health"

        service = JsonSchemaService()

        schema = Schema.objects.filter(label=schema_label).first()
        if not schema:
            schema = Schema.create_new_empty_schema(schema_label)

        # Takes to long time to do full
        service.write_to_db_baseschema(sample=True, positive_list=extras)

        DataCleaningService().relate_root_classes_to_foaf(schema)

        return schema

    @staticmethod
    def init_rdf_base():
        rdf_service = RdfSchemaService()

        rdf_service.write_to_db_baseschema()

    @classmethod
    def loadStravaActivities(cls):
        testfile = os.path.join(
            settings.BASE_DIR,
            "metadata/tests/data/json/strava_activities.json")
        data = JsonUtils.read_json_file(testfile)
        return data

    @classmethod
    def init_full(cls):
        cls.init_user()
        cls.init_rdf_base()
        cls.init_open_m_health_sample()
        cls.init_strava_schema_from_file()
        cls.init_strava_data_from_file()

    @classmethod
    def load_dummy_provider_json(cls):
        return {
            "provider_name": "strava3",
            "api_type": "OauthRest",
            "api_endpoint": "https://www.strava.com/api/",
            "authorize_url": "https://www.strava.com/oauth/authorize",
            "access_token_url": "https://www.strava.com/oauth/token",
            "client_id": "12345",
            "client_secret": "very_secret",
            "scope": ["scope1", "scope2", "scope3"],
            "endpoints": [
                {
                    "endpoint_name": "activity",
                    "endpoint_url": "v3/activities"
                },
                {
                    "endpoint_name": "zone",
                    "endpoint_url": "v3/athlete/zones"
                },
            ],
        }

    @classmethod
    def create_dummy_provider(cls, dp_profile):
        # TODO this should be refactored
        json_provider_obj = LoadTestData.load_dummy_provider_json()
        filter = SerializableModelFilter(start_object_name="data_provider")
        dp = DataProvider.deserialize(json_provider_obj, filter)
        dp.data_provider_profile = dp_profile
        dp.save()
        return dp_profile
