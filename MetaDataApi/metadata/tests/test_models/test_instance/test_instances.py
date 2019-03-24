import logging
import unittest

import django
from django.test import TransactionTestCase

from MetaDataApi.metadata.models import Object
from MetaDataApi.metadata.tests.data import LoadTestData
from MetaDataApi.metadata.tests.utils_for_testing.common_utils_for_testing import UtilsForTesting

logging.disable(logging.CRITICAL)


class TestModelInstances(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestModelInstances, cls).setUpClass()
        django.setup()

    @unittest.skip("needs repair")
    def test_get_related_list(self):
        from MetaDataApi.metadata.models import ObjectInstance
        schema = LoadTestData.init_foaf()
        obj = Object.objects.get(label="person", schema=schema)

        obj_inst = ObjectInstance(base=obj)
        res_inst = obj_inst.get_related_list()

        res = obj.get_related_list()

        res_string = list(map(lambda x: x.label, res))

        expected = [
            'person', 'person', 'document', 'document', 'document',
            'image', 'document', 'document', 'surname', 'first_name',
            'family_name', 'geekcode', 'myers_briggs', 'plan']

        res_string.sort()
        expected.sort()

        self.assertEqual(res_string, expected)

    @unittest.skip("needs repair")
    def test_attribute_exists(self):
        # Register your models here.
        from MetaDataApi.metadata.models import (
            # instances
            FloatAttributeInstance,
            StringAttributeInstance,
            IntAttributeInstance,
            BoolAttributeInstance,
            DateTimeAttributeInstance)

        LoadTestData.init_foaf()
        LoadTestData.init_strava_schema_from_file()
        LoadTestData.init_strava_data_from_file()

        types = (FloatAttributeInstance, StringAttributeInstance,
                 IntAttributeInstance, BoolAttributeInstance,
                 DateTimeAttributeInstance)

        att_lists = [inst_type.objects.all() for inst_type in types]

        # Flatten the list
        real_atts = [item for sublist in att_lists for item in sublist]

        # convert to appropriate args for testing if it exists
        positive_list = [[type(att), att.base.label, att.object.pk, att.value]
                         for att in real_atts]

        negative_list = [UtilsForTesting.mutate(
            elm) for elm in list(positive_list)]

        positive_res = [Instance.exists(*args)
                        for Instance, *args in positive_list]

        negative_res = [Instance.exists(*args)
                        for Instance, *args in negative_list]

        pos_type = [type(att).__name__ for att in positive_res]
        pos_type_expected = [type(att).__name__ for att in real_atts]

        self.assertEqual(pos_type, pos_type_expected)
        self.assertEqual(negative_res, len(negative_res) * [None, ])

    @unittest.skip("needs repair")
    def test_object_exists(self):
        # Register your models here.
        from MetaDataApi.metadata.tests.utils_for_testing.find_object_json_children import FindObjectJsonChildren

        LoadTestData.init_foaf()
        LoadTestData.init_strava_schema_from_file()
        LoadTestData.init_strava_data_from_file()

        data = LoadTestData.loadStravaActivities()

        finder = FindObjectJsonChildren("strava")
        childrenslist = finder.build_from_json(data)

        # convert to appropriate args for testing if it exists
        positive_list = [[obj, obj.base.label, children]
                         for obj, children in childrenslist]

        negative_list = [UtilsForTesting.mutate(
            elm) for elm in list(positive_list)]

        positive_res = [Instance.exists(*args)
                        for Instance, *args in positive_list]

        negative_res = [Instance.exists(*args)
                        for Instance, *args in negative_list]

        pos_type = [type(obj).__name__ for obj in positive_res]
        pos_type_expected = [type(obj).__name__ for obj, _ in childrenslist]

        self.assertEqual(pos_type, pos_type_expected)
        self.assertEqual(negative_res, len(negative_res) * [None, ])
