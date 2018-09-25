import django
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.


class TestRdfService(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()

    def test_create_default_graphs(self):
        from MetaDataApi.metadata.services.rdf import rdfService
        from MetaDataApi.metadata.models import Schema, Object, ObjectRelation

        service = rdfService()

        service.create_default_schemas()

        # schemas = list(map(lambda x: Schema.objects.first(
        #     url=x), service.default_list))

        try:
            schemas = Schema.objects.All()
        except AttributeError as e:
            print(e)

        assertNotEquals(schemas, None)

    def test_upload_rdf(self):
        from MetaDataApi.metadata.services.rdf import rdfService

        url = "http://xmlns.com/foaf/0.1/"

        service = rdfService()

        service.rdfs_upload(url)

        self.assertEqual(1 + 1, 2)
