# Create your tests here.
# Create your tests here.

import django
from django.test import TransactionTestCase


class TestDjangoDynamicModel(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDjangoDynamicModel, cls).setUpClass()
        django.setup()

    def test_simple(self):
        data = {"test": {
            "dummy1": 1,
            "dumm2": "test"
        }}
        from MetaDataApi.graph.services.DynamicModelMutantService import DynamicModelMutantService
        DynamicModelMutantService.create_from_data("test_root2", data)
