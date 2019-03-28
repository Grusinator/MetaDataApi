import unittest

import django
from django.test import TransactionTestCase


class TestExportSchemaService(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestExportSchemaService, cls).setUpClass()
        django.setup()

    @unittest.skip("https://medium.com/@l.peppoloni/how-to-mock-s3-services-in-python-tests-dd5851842946")
    def test_Export(self):
        from MetaDataApi.metadata.services import ExportSchemaService, BaseMetaDataService
        from MetaDataApi.metadata.models import Object, Attribute
        schema_label = "test_schema"
        schema = BaseMetaDataService.create_new_empty_schema(schema_label)

        test_obj = Object(label="test", schema=schema)
        test_obj.save()

        att = Attribute(label="att", object=test_obj)
        att.save()

        ExportSchemaService.execute({
            "schema_label": schema_label,
        })

        expected = ""

        self.assertEqual(schema.url, expected)
