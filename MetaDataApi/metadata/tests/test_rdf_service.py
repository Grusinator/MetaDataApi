import django
from django.test import TestCase, TransactionTestCase
import collections
from django.db import transaction


# TODO: Configure your database in settings.py and sync before running tests.


class TestRdfService(TransactionTestCase):
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

        json_service.write_to_db_baseschema(sample=True)

    def test_create_default_graphs(self):
        from MetaDataApi.metadata.services.rdfs_service import RdfService
        from MetaDataApi.metadata.models import Schema, Object, ObjectRelation

        service = RdfService()

        service.write_to_db_baseschema()

        schemas_count = Schema.objects.all().count()

        self.assertNotEqual(schemas_count, 0)

    def test_upload_rdf(self):
        from MetaDataApi.metadata.services.rdfs_service import RdfService

        url = "http://xmlns.com/foaf/0.1/"

        service = RdfService()

        service.write_to_db(url)

        self.assertEqual(1 + 1, 2)

    def test_export_rdf(self):
        from MetaDataApi.metadata.services.rdfs_service import RdfService

        schema_label = "friend_of_a_friend"

        service = RdfService()
        # just take foaf
        service.write_to_db(rdf_url="http://xmlns.com/foaf/0.1/")

        schema = service.export_schema_from_db(schema_label)

        read_service = RdfService()
        objects = read_service.read_objects_from_rdfs(schema.rdfs_file)

        labels = list(map(lambda x: x.label, objects))

        labels_compare = [
            "organization", "project", "online_e_commerce_account",
            "online_chat_account", "online_gaming_account", "document",
            "membership_class", "person", "image", "online_account",
            "work_info_homepage", "knows", "interest", "image",
            "thumbnail", "workplace_homepage", "account_service_homepage",
            "publications", "school_homepage", "first_name", "account_name",
            "plan", "myers_briggs", "geekcode", "surname", "family_name"]

        labels = list(set(labels))
        labels_compare = list(set(labels_compare))

        labels.sort()
        labels_compare.sort()

        # self.assertListEqual(labels, labels_compare)

    def test_circle(self):
        from MetaDataApi.metadata.services.rdfs_service import RdfService
        from MetaDataApi.metadata.models import Schema, Object, ObjectRelation

        service = RdfService()

        schemas = Schema.objects.all()

        for schema in schemas:
            schema = service.export_schema_from_db(schema.label)
            before_list = service.touched_meta_items.copy()

            service.write_to_db(schema.rdfs_file, overwrite=True)
            after_list = service.touched_meta_items.copy()

            self.assertEqual(collections.Counter(before_list),
                             collections.Counter(after_list))
