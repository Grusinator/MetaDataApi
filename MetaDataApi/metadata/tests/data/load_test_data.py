import json
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from MetaDataApi.metadata.models import Schema, ObjectRelation, Object, Attribute
from MetaDataApi.users.models import Profile


class LoadTestData:

    @staticmethod
    def init_user():
        from django.contrib.auth.models import User

        user = User(
            username="test",
            password="test1234"
        )

        try:
            user = User.objects.get(username=user.username)
        except:
            user.save()

        LoadTestData.init_profile(user)
        return user

    @staticmethod
    def init_profile(user):
        LoadTestData.init_foaf()
        from MetaDataApi.users.models import Profile
        profile = Profile(
            user=user,
        )
        try:
            return Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            profile.save()
        return profile

    @staticmethod
    def init_foaf():
        from MetaDataApi.metadata.services import (
            RdfSchemaService)
        rdf_service = RdfSchemaService()
        # just take foaf
        rdf_service.write_to_db(rdf_url="http://xmlns.com/foaf/0.1/")

        return rdf_service.schema

    @staticmethod
    def init_strava_data_provider_profile():
        LoadTestData.init_foaf()
        user = LoadTestData.init_user()
        from MetaDataApi.dataproviders.models.load_default_data_providers import InitializeDefaultDataProviders
        InitializeDefaultDataProviders.load()
        from MetaDataApi.users.models import DataProviderProfile
        from MetaDataApi.dataproviders.models import DataProvider

        dataproviderprofile = DataProviderProfile(
            provider=DataProvider.objects.get(provider_name="strava"),
            access_token="174323610143cdcd159f7792c1c4ec5637a96e12",
            profile=Profile.objects.get(user=user)
        )
        dataproviderprofile.save()
        return dataproviderprofile


    @staticmethod
    def init_meta_data_api():
        from MetaDataApi.metadata.services import (
            RdfSchemaService)
        rdf_service = RdfSchemaService()
        rdf_service.write_to_db(
            rdf_url="https://meta-data-api-storage-dev.s3.amazonaws.com/media/schemas/meta_data_api.ttl"
        )

        # TODO fix error in obj rel load, this is a temp fix
        schema = Schema.objects.get(label="meta_data_api")
        data_dump = Object.objects.get(schema=schema, label="endpoint_data_dump")
        ObjectRelation(
            schema=schema,
            label="has_generated",
            from_object=Object.objects.get(schema=schema, label="rest_endpoint"),
            to_object=data_dump
        ).save()

        att = Attribute.objects.get(label="data_dump_file", object=data_dump)
        att.data_type = "file"
        att.save()

        return rdf_service.schema

    @staticmethod
    def init_strava_schema_from_file():
        from MetaDataApi.metadata.services import (
            RdfInstanceService, DataCleaningService,
            JsonAnalyser
        )

        LoadTestData.init_foaf()

        rdf_inst = RdfInstanceService()

        data_cleaning = DataCleaningService()

        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        with open(testfile) as f:
            data = json.loads(f.read())

        service = JsonAnalyser()

        schema_label = "strava"
        label = "activities"

        schema = Schema.create_new_empty_schema(schema_label)

        user = LoadTestData.init_user()

        service.identify_from_json_data(
            data, schema, user, parrent_label=label)
        data_cleaning.relate_root_classes_to_foaf(schema)

        return schema

    @staticmethod
    def init_strava_data_from_file():
        from MetaDataApi.metadata.services import (
            JsonAnalyser
        )
        from MetaDataApi.metadata.models import Schema

        user = LoadTestData.init_user()

        service = JsonAnalyser()

        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        with open(testfile) as f:
            data = json.loads(f.read())

        schema = Schema.objects.get(label="strava")

        label = "activities"

        objects = service.identify_from_json_data(
            data, schema, parrent_label=label, owner=user)

        return objects

    @staticmethod
    def init_open_m_health_sample(extras=None):
        from MetaDataApi.metadata.services import (
            JsonSchemaService, DataCleaningService
        )

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
        from MetaDataApi.metadata.services import RdfSchemaService
        rdf_service = RdfSchemaService()

        rdf_service.write_to_db_baseschema()

    @classmethod
    def loadStravaActivities(cls):
        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        with open(testfile) as f:
            data = json.loads(f.read())
        return data

    @classmethod
    def init_full(cls):
        cls.init_user()
        cls.init_rdf_base()
        cls.init_open_m_health_sample()
        cls.init_strava_schema_from_file()
        cls.init_strava_data_from_file()
