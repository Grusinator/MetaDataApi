import django
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command

from MetaDataApi.metadata.tests import TestDataInits


class TestDataCleaningService(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDataCleaningService, cls).setUpClass()
        django.setup()

        # populate the database
        from MetaDataApi.metadata.services import RdfSchemaService
        from MetaDataApi.metadata.services import (
            JsonSchemaService
        )

        TestDataInits.init_foaf()

        TestDataInits.init_open_m_health_sample(extras=[
            "body-temperature-2.0.json",
            "body-temperature-2.x.json",
        ])

    def test_identify_json_data_sample(self):
        from MetaDataApi.metadata.services.data_cleaning_service import (
            DataCleaningService)

        from MetaDataApi.metadata.models import Schema, Object

        dc_service = DataCleaningService()

        schema_label = "open_m_health"
        schema = dc_service._try_get_item(Schema(label=schema_label))

        dc_service.relate_root_classes_to_foaf(schema)

        self.assertEqual(1 + 1, 2)
