import django
import os
import json
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command
from MetaDataApi.metadata.services.data_cleaning_service import (
    DataCleaningService
)
from django.conf import settings


class LoadTestData:

    @staticmethod
    def init_user():
        from django.contrib.auth.models import User

        user = User(
            username="test",
            password="test1234"
        )
        user.save()

        return user

    @staticmethod
    def init_foaf():
        from MetaDataApi.metadata.services import (
            RdfSchemaService)
        rdf_service = RdfSchemaService()
        # just take foaf
        rdf_service.write_to_db(rdf_url="http://xmlns.com/foaf/0.1/")

        return rdf_service.schema

    @staticmethod
    def init_strava_schema_from_file():
        from MetaDataApi.metadata.services import (
            RdfInstanceService, RdfSchemaService, DataCleaningService,
            SchemaIdentificationV2
        )

        from MetaDataApi.metadata.models import Schema, Object, Attribute

        LoadTestData.init_foaf()

        rdf_inst = RdfInstanceService()

        data_cleaning = DataCleaningService()

        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        with open(testfile) as f:
            data = json.loads(f.read())

        service = SchemaIdentificationV2()

        schema_label = "strava"
        label = "activities"

        schema = service.create_new_empty_schema(schema_label)

        service.identify_schema_from_dataV2(
            data, schema, parrent_label=label)

        data_cleaning.relate_root_classes_to_foaf(schema)

        return schema

    @staticmethod
    def init_strava_data_from_file():
        from MetaDataApi.metadata.services import (
            RdfInstanceService, RdfSchemaService, DataCleaningService,
            SchemaIdentificationV2
        )
        from MetaDataApi.metadata.models import Schema, Object, Attribute

        user = LoadTestData.init_user()

        service = SchemaIdentificationV2()

        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")
        with open(testfile) as f:
            data = json.loads(f.read())

        schema = service._try_get_item(Schema(label="strava"))

        label = "activities"

        objects = service.map_data_to_native_instances(
            data, schema, parrent_label=label, owner=user)

        return objects

    @staticmethod
    def init_open_m_health_sample(extras=None):
                # populate the database

        from MetaDataApi.metadata.services import (
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
        from MetaDataApi.metadata.services import RdfSchemaService
        rdf_service = RdfSchemaService()

        rdf_service.write_to_db_baseschema()

    @classmethod
    def init_full(cls):
        cls.init_user()
        cls.init_rdf_base()
        cls.init_open_m_health_sample()
        cls.init_strava_schema_from_file()
        cls.init_strava_data_from_file()
