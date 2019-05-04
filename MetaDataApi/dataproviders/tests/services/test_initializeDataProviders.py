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

        assert len(dpOs) == len(dps)
        assert len(dpOs) > 10

        self.assertListEqual([dp.provider_name for dp in dps], [dpO.provider_name.value for dpO in dpOs])
        self.assertListEqual([dp.client_id for dp in dps], [dpO.client_id for dpO in dpOs])
        self.assertListEqual(dps, [dpO.db_data_provider for dpO in dpOs])

    def test_get_providers_from_aws(self):
        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders

        json = InitializeDataProviders.get_providers_from_aws()
        assert json
