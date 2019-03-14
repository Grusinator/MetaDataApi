import json
import os

from django.conf import settings


class LoadTestData:

    @staticmethod
    def init_user():
        from django.contrib.auth.models import User

        user = User(
            username="test",
            password="test1234"
        )
        try:
            return User.objects.get(username=user.username)
        except:
            user.save()
            return user

    @staticmethod
    def init_foaf():
        from metadata.services import (
            RdfSchemaService)
        rdf_service = RdfSchemaService()
        # just take foaf
        rdf_service.write_to_db(rdf_url="http://xmlns.com/foaf/0.1/")

        return rdf_service.schema

    @staticmethod
    def init_strava_schema_from_file():
        from metadata.services import (
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

        schema = service.create_new_empty_schema(schema_label)

        user = LoadTestData.init_user()

        service.identify_from_json_data(
            data, schema, user, parrent_label=label)
        data_cleaning.relate_root_classes_to_foaf(schema)

        return schema

    @staticmethod
    def init_strava_data_from_file():
        from metadata.services import (
            JsonAnalyser
        )
        from metadata.models import Schema

        user = LoadTestData.init_user()

        service = JsonAnalyser()

        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        with open(testfile) as f:
            data = json.loads(f.read())

        schema = service.do_meta_item_exists(Schema(label="strava"))

        label = "activities"

        objects = service.identify_from_json_data(
            data, schema, parrent_label=label, owner=user)

        return objects

    @staticmethod
    def init_open_m_health_sample(extras=None):
        from metadata.services import (
            JsonSchemaService, DataCleaningService
        )

        schema_label = "open_m_health"

        service = JsonSchemaService()

        schema = service.create_new_empty_schema(schema_label)

        # Takes to long time to do full
        service.write_to_db_baseschema(sample=True, positive_list=extras)

        DataCleaningService().relate_root_classes_to_foaf(schema)

        return schema

    @staticmethod
    def init_rdf_base():
        from metadata.services import RdfSchemaService
        rdf_service = RdfSchemaService()

        rdf_service.write_to_db_baseschema()

    @classmethod
    def init_full(cls):
        cls.init_user()
        cls.init_rdf_base()
        cls.init_open_m_health_sample()
        cls.init_strava_schema_from_file()
        cls.init_strava_data_from_file()
