import django
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command
from datetime import datetime

from MetaDataApi.datapoints.services import GetTemporalFloatPairsService
from MetaDataApi.metadata.tests import TestDataInits


class TestSomeService(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestSomeService, cls).setUpClass()
        django.setup()

    def test_some(self):

        TestDataInits.init_strava_schema_from_file()
        TestDataInits.init_strava_data_from_file()

        args = {
            "schema_label": "strava",
            "object_label": "activities",
            "attribute_label": "distance",
            "datetime_label": "name",
            "datetime_object_label": "activities",
        }

        data = GetTemporalFloatPairsService.execute(args)

        expected = []

        self.assertListEqual(data, expected)
