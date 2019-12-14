import unittest

import django
from django.test import TransactionTestCase


class TestStoreDataFromProviderService(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestStoreDataFromProviderService, cls).setUpClass()
        django.setup()

    @unittest.skip(
        "excluded since it is not relevant untill it has been implemented as a dynamic model thing/interface")
    def test_store_data_from_provider_service(self):
        pass
        # from dataproviders.services.services import StoreDataFromProviderService
        #
        # from dataproviders.models.initialize_data_providers import InitializeDataProviders
        # from metadata.models import FileAttribute
        # from metadata.tests import LoadTestData
        #
        # user = LoadTestData.init_user()
        # InitializeDataProviders.load()
        #
        # dpp = LoadTestData.init_strava_data_provider_profile()
        # LoadTestData.create_dummy_provider(dpp)
        #
        # data = StoreDataFromProviderService.execute({
        #     "provider_name": dpp.data_provider.provider_name,
        #     "endpoint_name": "activity",
        #     "user_pk": user.pk
        # })

        # data = JsonUtils.validate(data)
        #
        # fileAtt = FileAttribute.objects.get()
        #
        # file_as_str = fileAtt.read_as_str()
        # file = JsonUtils.validate(file_as_str)
        #
        # self.assertEqual(data, file)
