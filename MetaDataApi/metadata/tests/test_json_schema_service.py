import django
from django.test import TestCase, TransactionTestCase


# TODO: Configure your database in settings.py and sync before running tests.


class TestJsonService(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()
        super(TestJsonService, cls).setUpClass()

        # populate the database
        from MetaDataApi.metadata.services.rdfs_service import RdfService
        from MetaDataApi.metadata.services.json_schema_service import (
            JsonSchemaService
        )
        rdf_service = RdfService()

        rdf_service.write_to_db_baseschema()

        service = JsonSchemaService()
        # Takes to long time to do full
        service.write_to_db_baseschema(sample=True)

    def test_upwrite_to_db(self):
        from MetaDataApi.metadata.services.json_schema_service import (
            JsonSchemaService)

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/" +\
            "master/schemas/json/omh/schemas/acceleration-1.0.json"

        service = JsonSchemaService()

        res = service.write_to_db(url, "openMHealth")

    def test_json_write_to_db_body_temp(self):
        from MetaDataApi.metadata.services.json_schema_service import (
            JsonSchemaService)
        from MetaDataApi.metadata.models import (
            Schema, Object, Attribute, ObjectRelation)

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/" +\
            "master/schemas/json/omh/schemas/body-temperature-2.0.json"

        service = JsonSchemaService()

        res = service.write_to_db(url, "openMHealth")

        atts = filter(lambda x: isinstance(x, Attribute), res)

    def test_default_schemas(self):
        from MetaDataApi.metadata.services.json_schema_service import (
            JsonSchemaService)

        service = JsonSchemaService()
        # Takes to long time to do full
        service.write_to_db_baseschema(sample=True)
