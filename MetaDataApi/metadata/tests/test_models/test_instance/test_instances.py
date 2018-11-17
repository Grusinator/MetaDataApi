import django
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command

from MetaDataApi.metadata.tests import TestDataInits


class TestModelInstances(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestModelInstances, cls).setUpClass()
        django.setup()

        # populate the database
        from MetaDataApi.metadata.services import (
            RdfSchemaService,
            JsonSchemaService
        )

        TestDataInits.init_foaf()

        TestDataInits.init_open_m_health_sample(extras=[
            "body-temperature-2.0.json",
            "body-temperature-2.x.json",
        ])

    def test_attribute_exists(self):
        # Register your models here.
        from MetaDataApi.metadata.models.instances import (
            # instances
            ObjectInstance,
            ObjectRelationInstance,
            FloatAttributeInstance,
            StringAttributeInstance,
            IntAttributeInstance,
            BoolAttributeInstance,
            ImageAttributeInstance)

        TestDataInits.init_strava_schema_from_file()
        TestDataInits.init_strava_data_from_file()

        test_list = [
            (FloatAttributeInstance, "testlabel", 1000, "some value")
        ]

        res = [Instance(*args) for Instance, *args value in test_list]

        expected = [None]

        self.assertEqual(res, expected)
