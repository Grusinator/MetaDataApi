import unittest

import django
from django.test import TransactionTestCase

from MetaDataApi.metadata.models import Schema


class TestExportSchemaService(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestExportSchemaService, cls).setUpClass()
        django.setup()

    @unittest.skip("https://medium.com/@l.peppoloni/how-to-mock-s3-services-in-python-tests-dd5851842946")
    def test_Export(self):
        from MetaDataApi.metadata.services import ExportSchemaService
        from MetaDataApi.metadata.models import SchemaNode, SchemaAttribute
        schema_label = "test_schema"
        schema = Schema.create_new_empty_schema(schema_label)

        test_obj = SchemaNode(label="test", schema=schema)
        test_obj.save()

        att = SchemaAttribute(label="att", object=test_obj)
        att.save()

        ExportSchemaService.execute({
            "schema_label": schema_label,
        })

        expected = ""

        self.assertEqual(schema.url, expected)
