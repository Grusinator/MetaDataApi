import django
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command
from MetaDataApi.metadata.services import BaseMetaDataService

from MetaDataApi.metadata.tests import TestDataInits

from MetaDataApi.metadata.services import *


class TestServices(TransactionTestCase):
    """Tests for the application views."""
    # fixtures = [
    #     'metadata/fixtures/new_load.json',
    # ]

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestServices, cls).setUpClass()
        django.setup()

    def DeleteSchemaServiceTest(self):

        TestDataInits.init_strava_schema_from_file()

        args = {
            schema_label: "strava",
        }

        data = DeleteSchemaService.execute(args)

        schema = next(Schema.objects.filter(label="strava"))

        self.assertIsNone(schema)
