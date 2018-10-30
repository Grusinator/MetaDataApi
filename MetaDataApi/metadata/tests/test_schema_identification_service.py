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


class TestSchemaIdentificationService(TransactionTestCase):
    """Tests for the application views."""
    # fixtures = [
    #     'metadata/fixtures/new_load.json',
    # ]

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestSchemaIdentificationService, cls).setUpClass()
        django.setup()

        # call_command(
        #     'loaddata',
        #     'metadata/fixtures/new_load.json',
        #     verbosity=0
        # )
        # call_command('loaddata', 'fixtures/testdb.json', verbosity=1)

        # populate the database
        from MetaDataApi.metadata.services import RdfSchemaService
        from MetaDataApi.metadata.services import (
            JsonSchemaService
        )
        from MetaDataApi.metadata.models import Schema, Object

        rdf_service = RdfSchemaService()

        # just take foaf
        rdf_service.write_to_db(rdf_url="http://xmlns.com/foaf/0.1/")

        json_service = JsonSchemaService()

        # this takes to long time if doing full
        json_service.write_to_db_baseschema(positive_list=[
            "body-temperature-2.0.json",
            "body-temperature-2.x.json",
        ])

        dc_service = DataCleaningService()

        schema_label = "open_m_health"
        schema = dc_service._try_get_item(Schema(label=schema_label))

        dc_service.relate_root_classes_to_foaf(schema)

    def test_identify_json_data_sample(self):
        from MetaDataApi.metadata.services import (
            SchemaIdentificationV2)

        from MetaDataApi.metadata.models import Schema, Object

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi" + \
            "/master/schemas/json/omh/test_data/body-temperature/2.0/" + \
            "shouldPass/valid-temperature.json"

        obj_count = Object.objects.all().count()
        # make sure that the number of objects is larger than
        if obj_count < 10:
            raise AssertionError("database not populated")

        with request.urlopen(url) as resp:
            text = resp.read().decode()

        service = SchemaIdentificationV2()
        schema = service._try_get_item(Schema(label="open_m_health"))

        input_data = {
            "body-temperature": json.loads(text)
        }

        resp, objs = service.map_data_to_native_instances(input_data, schema)

        self.assertEqual(len(objs), 4)


class NoDataTestSchemaIdentificationService(TransactionTestCase):
    """Tests for the application views."""
    # fixtures = [
    #     'metadata/fixtures/new_load.json',
    # ]

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(NoDataTestSchemaIdentificationService, cls).setUpClass()
        django.setup()

    def test_identify_datatype(self):
        from MetaDataApi.metadata.services import (
            SchemaIdentificationV2)
        from datetime import datetime

        input_vs_expected = [
            ("20.40", float),
            (2.4, float),
            ("2012-01-19 17:21:00", datetime),
            # ("2019-20-04:20:30:59", datetime),
            (2, int),
            ("1", int),
            ("test", str),
            ("False", bool),
            (True, bool),
            (None, type(None))
        ]

        inputd, expected = zip(*input_vs_expected)

        service = SchemaIdentificationV2()

        resp = [type(service.identify_datatype(elm)) for elm in inputd]

        self.assertListEqual(list(resp), list(expected))

    def test_identify_json_data_strava_test(self):
        from MetaDataApi.metadata.services import (
            RdfSchemaService, DataCleaningService,
            SchemaIdentificationV2, RdfInstanceService)

        from MetaDataApi.metadata.models import Schema, Object
        from django.contrib.auth.models import User

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

        user = User(
            username="test",
            password="dummy1234"
        )
        user.save()

        schema = service._try_get_item(Schema(label=schema_label))

        service.identify_schema_from_dataV2(
            data, schema, parrent_label=label)

        data_cleaning.relate_root_classes_to_foaf(schema)

        _, objects = service.map_data_to_native_instances(
            data, schema, parrent_label=label, owner=user)

        rdf_service.export_schema_from_db(schema)
        fiel = rdf_inst.export_instances_to_rdf_file(schema, objects)

        print(service.schema.url)

        self.assertGreater(len(objects), 10)
