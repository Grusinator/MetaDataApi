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
        from MetaDataApi.metadata.services.jsonschema import JsonSchemaService

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas/json/omh/acceleration-1.0.json"

        service = JsonSchemaService()

        service.load_json_schema(url, "openMHealth")
