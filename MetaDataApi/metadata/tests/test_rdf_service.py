import django
from django.test import TestCase
import collections
from django.db import transaction


# TODO: Configure your database in settings.py and sync before running tests.


class TestRdfService(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        django.setup()
        super(TestRdfService, cls).setUpClass()

        # populate the database
        from MetaDataApi.metadata.services.rdfs_service import RdfService
        from MetaDataApi.metadata.services.json_schema_service import (
            JsonSchemaService
        )
        rdf_service = RdfService()

        rdf_service.write_to_db_baseschema()

        json_service = JsonSchemaService()

        # json_service.write_to_db_baseschema()

    def test_create_default_graphs(self):
        from MetaDataApi.metadata.services.rdfs_service import RdfService
        from MetaDataApi.metadata.models import Schema, Object, ObjectRelation

        service = RdfService()

        service.write_to_db_baseschema()

        # schemas = list(map(lambda x: Schema.objects.first(
        #     url=x), service.default_list))

        schemas_count = Schema.objects.all().count()

        self.assertNotEqual(schemas_count, 0)

    def test_upload_rdf(self):
        from MetaDataApi.metadata.services.rdfs_service import RdfService

        url = "http://xmlns.com/foaf/0.1/"

        service = RdfService()

        service.write_to_db(url)

        self.assertEqual(1 + 1, 2)

    def test_circle(self):
        from MetaDataApi.metadata.services.rdfs_service import RdfService
        from MetaDataApi.metadata.models import Schema, Object, ObjectRelation

        service = RdfService()

        schemas = Schema.objects.all()

        for schema in schemas:
            schema = service.export_schema_from_db(schema.label)
            before_list = service._objects_created_list.copy()

            service.write_to_db(schema.rdfs_file, overwrite=True)
            after_list = service._objects_created_list.copy()

            self.assertEqual(collections.Counter(before_list),
                             collections.Counter(after_list))
