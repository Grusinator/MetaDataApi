import django
from django.test import TestCase, TransactionTestCase

from MetaDataApi.metadata.tests import TestDataInits


class TestJsonUtils(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestJsonUtils, cls).setUpClass()
        django.setup()

    def test_identify_json_data_sample(self):

        self.assertEqual(1 + 1, 2)
