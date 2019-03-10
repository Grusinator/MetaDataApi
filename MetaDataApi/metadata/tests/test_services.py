import os

import django
from django.test import TransactionTestCase

import settings
from metadata.tests.data import LoadTestData
from tests import TestServices


class TestMetaServices(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestServices, cls).setUpClass()
        django.setup()

    def DeleteSchemaServiceTest(self):
        from metadata.models import Schema
        from metadata.services.services import DeleteSchemaService
        LoadTestData.init_strava_schema_from_file()

        args = {
            "schema_label": "strava",
        }

        data = DeleteSchemaService.execute(args)

        schema = next(Schema.objects.filter(label="strava"))

        self.assertIsNone(schema)

    def IdentifyDataFromProviderServiceTest(self):
        LoadTestData.init_strava_schema_from_file()
        user = LoadTestData.init_user()

        # # will fail since third party profile is not defined
        # args = {
        #     "provider_name": thd_part_profile.provider.provider_name,
        #     "endpoint": "all",
        #     "user_pk": thd_part_profile.profile.user.pk,
        # }
        #
        # data = IdentifyDataFromProviderService.execute(args)
        #
        # self.assertIsNone(schema)

    def IdentifyDataFromFileServiceTest(self):
        from metadata.services.services import IdentifyDataFromFileService
        LoadTestData.init_strava_schema_from_file()
        user = LoadTestData.init_user()
        # will fail since third party profile is not defined
        # load the file
        testfile = os.path.join(
            settings.BASE_DIR,
            "MetaDataApi/metadata/tests/data/json/strava_activities.json")

        args = {
            "schema_label": "strava",
            "data_label": "activities",
            "user_pk": user.pk,
        }

        with open(testfile) as datafile:
            data = IdentifyDataFromFileService.execute(args, files=datafile)

        self.assertIsNotNone(data)
