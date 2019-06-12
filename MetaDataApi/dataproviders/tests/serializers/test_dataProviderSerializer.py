import django
from django.test import TransactionTestCase

from MetaDataApi.dataproviders.serializers.DataProviderSerializer import DataProviderSerializer


class TestDataProviderSerializer(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestDataProviderSerializer, cls).setUpClass()
        django.setup()

    def test_serializing(self):
        from MetaDataApi.dataproviders.models import DataProvider
        dp = DataProvider.objects.create(
            provider_name="dsfsd"
        )

        data = DataProviderSerializer(dp)
        self.assertEqual("", data)
