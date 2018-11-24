from MetaDataApi.metadata.tests.data import LoadTestData
from django.test import TestCase, TransactionTestCase
import django

from MetaDataApi.metadata.tests import utils_for_testing
from MetaDataApi.metadata.utils.django_model_utils import BuildDjangoSearchArgs


class TestBuildDjangoSearchArgs(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestBuildDjangoSearchArgs, cls).setUpClass()
        # django.setup()

    def test_build_search_args_from_json(self):

        #data = UtilsForTesting.loadStravaActivities()

        data = {
            "object1": {
                "Attribute1": 3,
                "Attribute2": {"value": "att2value"},
                "object2": {
                    "attribute3": True,
                    "attribute4": 5.04
                }
            }
        }

        builder = BuildDjangoSearchArgs()
        args = builder.build_from_json(data)

        expected = {
            'from_relations__from_object__label': 'object1',
            'from_relations__from_object__from_relations__from_object__label__in':
                ['Attribute1',
                 'Attribute2',
                 'object2'],
            'from_relations__from_object__from_relations__from_object__from_relations__from_object__label__in':
                ['attribute3',
                 'attribute4']
        }

        self.assertEqual(args, expected)
