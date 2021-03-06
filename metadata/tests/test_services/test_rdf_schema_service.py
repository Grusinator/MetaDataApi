import unittest

import django
from django.conf import settings
from django.test import TransactionTestCase

from MetaDataApi.utils.unittest_utils.unittest_utils import UnittestUtils
from metadata.tests.data import LoadTestData

TAGS = set("rdf")


class TestRdfSchemaService(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestRdfSchemaService, cls).setUpClass()
        django.setup()

    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    def test_create_default_graphs(self):
        from metadata.services import RdfSchemaService
        from metadata.models import Schema

        service = RdfSchemaService()

        service.write_to_db_baseschema()

        schemas_count = Schema.objects.all().count()

        self.assertNotEqual(schemas_count, 0)

    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    def test_upload_rdf(self):
        from metadata.services import RdfSchemaService
        from metadata.models.meta import Schema, SchemaNode, SchemaAttribute

        url = "http://xmlns.com/foaf/0.1/"

        service = RdfSchemaService()

        service.write_to_db(url)

        self.assertIsNotNone(
            Schema.objects.get(label="friend_of_a_friend"))
        self.assertIsNotNone(SchemaNode.objects.filter(label="person").first())
        self.assertIsNotNone(SchemaNode.objects.filter(label="project").first())
        self.assertIsNotNone(SchemaNode.objects.filter(label="image").first())
        self.assertIsNotNone(SchemaAttribute.objects.filter(
            label="first_name").first())

    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    @unittest.skip("check later after merging dynamic model aproach")
    def test_export_rdf(self):
        from metadata.services import RdfSchemaService

        service = RdfSchemaService()

        schema = LoadTestData.init_foaf()

        schema = service.export_schema_from_db(schema)

        read_service = RdfSchemaService()

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

        self.assertListEqual(labels, labels_compare)

    @unittest.skipIf(set(settings.TEST_SETTINGS_EXCLUDE) & TAGS, f"skipping: {settings.TEST_SETTINGS_EXCLUDE}")
    @unittest.skip("check later after merging dynamic model aproach")
    def test_circle(self):
        from metadata.services import RdfSchemaService
        from metadata.models import Schema

        LoadTestData.init_rdf_base()
        # LoadTestData.init_open_m_health_sample()

        service = RdfSchemaService()

        schemas = Schema.objects.all()

        for schema in schemas:
            schema = service.export_schema_from_db(schema)
            before_list = service.touched_meta_items.copy()
            before_list = UnittestUtils.build_meta_instance_strings_for_comparison(before_list)

            service.write_to_db(schema.rdfs_file, overwrite=True)
            after_list = service.touched_meta_items.copy()
            after_list = UnittestUtils.build_meta_instance_strings_for_comparison(after_list)

            self.assertListEqual(before_list, after_list)
