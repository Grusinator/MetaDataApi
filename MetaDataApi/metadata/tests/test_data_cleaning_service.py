import django
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command


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

        rdf_service = RdfSchemaService()

        # just take foaf
        rdf_service.write_to_db(rdf_url="http://xmlns.com/foaf/0.1/")

        json_service = JsonSchemaService()

        # this takes to long time if doing full
        json_service.write_to_db_baseschema(positive_list=[
            "body-temperature-2.0.json",
            "body-temperature-2.x.json",
        ])

    def test_identify_json_data_sample(self):
        from MetaDataApi.metadata.services.data_cleaning_service import (
            DataCleaningService)

        from MetaDataApi.metadata.models import Schema, Object

        service = DataCleaningService()

        resp = service.relate_root_classes_to_foaf("open_m_health")

        self.assertEqual(1 + 1, 2)
