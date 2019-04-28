import django
from django.test import TransactionTestCase


class TestInitializeDataProviders(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestInitializeDataProviders, cls).setUpClass()
        django.setup()

    def test_load_from_json(self):
        from MetaDataApi.metadata.rdfs_models.initialize_rdf_models import InitializeRdfModels
        InitializeRdfModels.create_all_schemas()

        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders
        InitializeDataProviders.load_from_json()

        from MetaDataApi.dataproviders.models import DataProvider
        dps = list(DataProvider.objects.all())

        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import DataProviderO
        dpOs = [DataProviderO(dp.data_provider_instance.pk) for dp in dps]

        self.assertEqual(dps, None)
