import django
from django.test import TransactionTestCase


class TestStoreDataFromProviderService(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestStoreDataFromProviderService, cls).setUpClass()
        django.setup()

    def test_store_data_from_provider_service(self):
        from MetaDataApi.dataproviders.services.services import StoreDataFromProviderService

        from MetaDataApi.dataproviders.models.load_default_data_providers import InitializeDefaultDataProviders
        from MetaDataApi.metadata.models import FileAttributeInstance
        from MetaDataApi.metadata.tests import LoadTestData
        from MetaDataApi.metadata.rdf_models.initialize_rdf_models import InitializeRdfModels
        user = LoadTestData.init_user()
        InitializeRdfModels.create_all_schemas()
        InitializeDefaultDataProviders.load()

        dpp = LoadTestData.init_strava_data_provider_profile()

        data = StoreDataFromProviderService.execute({
            "provider_name": dpp.provider.provider_name,
            "endpoint_name": "activity",
            "user_pk": user.pk
        })

        fileAtt = FileAttributeInstance.objects.get()

        file = fileAtt.value.file.read()

        self.assertEqual(data, file)
