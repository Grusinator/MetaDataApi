import django
from django.test import TransactionTestCase

from MetaDataApi.metadata.utils.testing_utils import TestingUtils


class TestInitializeRdfModels(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestInitializeRdfModels, cls).setUpClass()
        django.setup()

    def test_create_all_schemas_from_descriptor(self):
        from MetaDataApi.metadata.rdfs_models.initialize_rdf_models import InitializeRdfModels
        InitializeRdfModels.create_all_schemas_from_descriptor()

        labels = TestingUtils.get_all_item_labels_from_schema("meta_data_api")
        expected = ['access_token_url', 'api_endpoint', 'api_type', 'api_type', 'authorize_url', 'client_id',
                    'client_secret', 'data_provider_has_endpoint', 'data_provider_name', 'datadump', 'dataprovidero',
                    'date_downloaded', 'endpoint', 'endpoint_name', 'endpoint_url', 'file', 'file_origin_url',
                    'has_data_dump', 'loaded', 'meta_data_api', 'scope']
        self.assertListEqual(expected, labels)
