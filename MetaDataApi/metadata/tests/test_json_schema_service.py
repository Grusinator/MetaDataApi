import django
from django.test import TestCase


# TODO: Configure your database in settings.py and sync before running tests.


class TestRdfService(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestRdfService, cls).setUpClass()
        django.setup()

    def test_upload_json_schema(self):
        from MetaDataApi.metadata.services.json_schema_service import JsonSchemaService

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas/json/omh/schemas/acceleration-1.0.json"

        service = JsonSchemaService()

        res = service.load_json_schema(url, "openMHealth")

    def test_upload_json_schema_body_temp(self):
        from MetaDataApi.metadata.services.json_schema_service import JsonSchemaService
        from MetaDataApi.metadata.models import (
            Schema, Object, Attribute, ObjectRelation)

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas/json/omh/schemas/body-temperature-2.0.json"

        service = JsonSchemaService()

        res = service.load_json_schema(url, "openMHealth")

        atts = filter(lambda x: isinstance(x, Attribute), res)

    def test_default_schemas(self):
        from MetaDataApi.metadata.services.json_schema_service import JsonSchemaService

        service = JsonSchemaService()
        service.write_to_db_baseschema()
