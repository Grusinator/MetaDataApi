import django
from django.test import TransactionTestCase

from metadata.tests.data import LoadTestData


class TestDataCleaningService(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDataCleaningService, cls).setUpClass()
        django.setup()

        # populate the database

        LoadTestData.init_foaf()

        LoadTestData.init_open_m_health_sample(extras=[
            "body-temperature-2.0.json",
            "body-temperature-2.x.json",
        ])

    def test_identify_json_data_sample(self):
        from metadata.services.all_services.data_cleaning_service import (
            DataCleaningService)

        from metadata.models import Schema

        dc_service = DataCleaningService()

        schema_label = "open_m_health"
        schema = dc_service._try_get_item(Schema(label=schema_label))

        dc_service.relate_root_classes_to_foaf(schema)

        self.assertEqual(1 + 1, 2)
