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

from MetaDataApi.metadata.tests import TestDataInits


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

    def test_identify_json_data_sample(self):
        from MetaDataApi.metadata.services import (
            SchemaIdentificationV2)

        from MetaDataApi.metadata.models import Schema, Object

        TestDataInits.init_foaf()

        TestDataInits.init_open_m_health_sample(extras=[
            "body-temperature-2.0.json",
            "body-temperature-2.x.json",
        ])

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

        objs = service.map_data_to_native_instances(input_data, schema)

        self.assertEqual(len(objs), 4)

    def test_identify_datatype(self):
        from MetaDataApi.metadata.services import (
            SchemaIdentificationV2)
        from datetime import datetime

        input_vs_expected = [
            ("20.40", float),
            (2.4, float),
            ("2012-01-19 17:21:00", datetime),
            ('2018-10-02T16: 16: 49Z', datetime),
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

        rdf_inst = RdfInstanceService()

        data_cleaning = DataCleaningService()

        TestDataInits.init_foaf()

        schema = TestDataInits.init_strava_schema_from_file()

        objects = TestDataInits.init_strava_data_from_file()

        RdfSchemaService().export_schema_from_db(schema)

        file = RdfInstanceService().export_instances_to_rdf_file(schema, objects)

        print(schema.url)

        self.assertGreater(len(objects), 10)
