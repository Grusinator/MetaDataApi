import django
from django.test import TransactionTestCase


class TestStoreDataFromProviderService(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestStoreDataFromProviderService, cls).setUpClass()
        django.setup()

    def test_store_data_from_provider_service(self):
        from MetaDataApi.dataproviders.services.services import StoreDataFromProviderService

        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders
        from MetaDataApi.metadata.models import FileAttributeInstance
        from MetaDataApi.metadata.tests import LoadTestData
        from MetaDataApi.metadata.rdfs_models.initialize_rdf_models import InitializeRdfModels
        user = LoadTestData.init_user()
        InitializeRdfModels.create_all_schemas()
        InitializeDataProviders.load()

        dpp = LoadTestData.init_strava_data_provider_profile()

        data = StoreDataFromProviderService.execute({
            "provider_name": dpp.provider.provider_name,
            "endpoint_name": "activity",
            "user_pk": user.pk
        })

        fileAtt = FileAttributeInstance.objects.get()

        file = fileAtt.value.file.read()

        self.assertEqual(data, file)
