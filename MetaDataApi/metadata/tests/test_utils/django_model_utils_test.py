from MetaDataApi.metadata.tests import TestDataInits
from django.test import TestCase, TransactionTestCase
import django

from MetaDataApi.metadata.utils import DjangoModelUtils, TestingUtils


class TestBuildSearchArgsFromJson(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestBuildSearchArgsFromJson, cls).setUpClass()
        # django.setup()

    def test_BuildSearchArgsFromJson(self):

        data = TestingUtils.loadStravaActivities()

        args = DjangoModelUtils.BuildSearchArgsFromJson().build_search_args_from_json()

        self.assertEqual(args, 2)
