import unittest

import django
from django.test import TransactionTestCase

from metadata.tests.data import LoadTestData


class TestMetadataBaseFunctionService(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestMetadataBaseFunctionService, cls).setUpClass()
        django.setup()

    @unittest.skip("maximum recursion")
    def test_path_to_foaf_person(self):
        from metadata.services.services import BaseMetaDataService
        from metadata.models import (
            SchemaNode, SchemaAttribute)

        LoadTestData.init_foaf()

        att = SchemaAttribute(object=SchemaNode.objects.get(label="image"),
                              label="test_att",
                              data_type="float")
        att.save()
        service = BaseMetaDataService()
        foaf, to_foaf_p_list = service.path_to_object(
            att, service.get_foaf_person())

        self.assertListEqual(to_foaf_p_list, [att, att.object, ])

    @unittest.skip("needs repair")
    def test_get_connected_pair(self):
        from metadata.models import SchemaAttribute
        from metadata.services import BaseMetaDataService
        LoadTestData.init_strava_schema_from_file()
        LoadTestData.init_strava_data_from_file()

        att1 = SchemaAttribute.objects.get(
            label="name", object__schema__label="strava")
        att2 = SchemaAttribute.objects.get(
            label="distance", object__schema__label="strava")

        data = BaseMetaDataService.get_connected_attribute_pairs(att1, att2)

        expected = []

        self.assertListEqual(data, expected)
