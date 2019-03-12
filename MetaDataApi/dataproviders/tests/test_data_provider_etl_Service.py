from datetime import datetime

import django
from django.test import TransactionTestCase


class TestDataProviderEtlService(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDataProviderEtlService, cls).setUpClass()
        django.setup()

    def test(self):
        from dataproviders.services import (
            DataProviderEtlService)

        from dataproviders.models import third_party_data_provider

        data_provider = third_party_data_provider(
            provider_name="dummy")
        # init service
        service = DataProviderEtlService(data_provider)

        start_time = datetime(2018, 3, 4)
        end_time = datetime(2018, 5, 4)

        endpoint = "testendpoint?start={StartDateTime:UTCSEC}&end={EndDateTime:UTCSEC}"

        output_endpoint = service.build_args_for_url(
            endpoint, StartDateTime=start_time, EndDateTime=end_time)

        expected = "testendpoint?start=1520118000&end=1525384800"

        self.assertEqual(output_endpoint, expected)
