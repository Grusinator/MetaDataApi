import django
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command

from MetaDataApi.metadata.tests.data import LoadTestData
from MetaDataApi.metadata.tests import UtilsForTesting


class TestModelInstances(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestModelInstances, cls).setUpClass()
        django.setup()

    def test_attribute_exists(self):
        # Register your models here.
        from MetaDataApi.metadata.models.instances import (
            # instances
            ObjectInstance,
            ObjectRelationInstance,
            FloatAttributeInstance,
            StringAttributeInstance,
            IntAttributeInstance,
            BoolAttributeInstance,
            ImageAttributeInstance,
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

  def test_attribute_exists(self):
        # Register your models here.
        from MetaDataApi.metadata.models.instances import ObjectInstance
       

        LoadTestData.init_foaf()
        LoadTestData.init_strava_schema_from_file()
        LoadTestData.init_strava_data_from_file()


        objects = ObjectInstance.objects.all()


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
