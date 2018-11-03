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


class TestDataInits:

    @staticmethod
    def init_base():
        from django.contrib.auth.models import User

        user = User(
            username="test",
            password="dummy1234"
        )
        user.save()

    @staticmethod
    def init_strava_data_from_file():
        from MetaDataApi.metadata.services import (
            RdfInstanceService, RdfSchemaService, DataCleaningService,
            SchemaIdentificationV2
        )

        from MetaDataApi.metadata.models import Schema, Object, Attribute

        user = TestDataInits.init_base()

        rdf_service = RdfSchemaService()
        rdf_inst = RdfInstanceService()

        data_cleaning = DataCleaningService()

        # just take foaf
        rdf_service.write_to_db(rdf_url="http://xmlns.com/foaf/0.1/")

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

        objects = service.map_data_to_native_instances(
            data, schema, parrent_label=label, owner=user)
