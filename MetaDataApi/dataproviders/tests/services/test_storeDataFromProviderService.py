import django
from django.test import TransactionTestCase

from MetaDataApi.metadata.utils import JsonUtils


class TestStoreDataFromProviderService(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestStoreDataFromProviderService, cls).setUpClass()
        django.setup()

    def test_store_data_from_provider_service(self):
        from MetaDataApi.dataproviders.services.services import StoreDataFromProviderService

        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders
        from MetaDataApi.metadata.models import FileAttribute
        from MetaDataApi.metadata.tests import LoadTestData

        user = LoadTestData.init_user()
        InitializeDataProviders.load()

        dpp = LoadTestData.init_strava_data_provider_profile()
        LoadTestData.create_dummy_provider(dpp)

        data = StoreDataFromProviderService.execute({
            "provider_name": dpp.provider.provider_name,
            "endpoint_name": "activity",
            "user_pk": user.pk
        })

        data = JsonUtils.validate(data)

        fileAtt = FileAttribute.objects.get()

        file_as_str = fileAtt.read_as_str()
        file = JsonUtils.validate(file_as_str)

        self.assertEqual(data, file)
