import django
from django.test import TransactionTestCase


class TestInitializeRdfModels(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestInitializeRdfModels, cls).setUpClass()
        django.setup()

    def test_create_all_schemas_from_descriptor(self):
        from MetaDataApi.metadata.rdfs_models.initialize_rdf_models import InitializeRdfModels
        InitializeRdfModels.create_all_schemas_from_descriptor()
