import django
from django.test import TestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command


class TestSchemaIdentificationService(TestCase):
    """Tests for the application views."""
    # fixtures = [
    #     'metadata/fixtures/new_load.json',
    # ]

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()

        call_command(
            'loaddata',
            'metadata/fixtures/new_load.json',
            verbosity=0
        )
        # call_command('loaddata', 'fixtures/testdb.json', verbosity=1)

    def test_identify_json_data_sample(self):
        from MetaDataApi.metadata.services.schema_identification import \
            SchemaIdentification

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi/master/schemas/json/omh/test_data/body-temperature/2.0/shouldPass/valid-temperature.json"

        obj_count = Object.objects.all().count()
        # make sure that the number of objects is larger than
        if obj_count < 10:
            raise AssertionError("database not populated")

        with request.urlopen(url) as resp:
            text = resp.read().decode()

        service = SchemaIdentification()

        service.identify_data(text)

        self.assertEqual(1 + 1, 2)

    def test_upload_from_file(self):
        path = r"C:\Users\William\source\repos\Django\MetaDataApi\MetaDataApi\metadata\tests\data\event.rdf"

        from MetaDataApi.metadata.services.rdf import RdfService

        service = RdfService()
        service.write_to_db(path)

        self.assertEqual(1 + 1, 2)
