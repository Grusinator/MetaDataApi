import django
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command
from datetime import datetime


class TestService(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestService, cls).setUpClass()
        django.setup()

    def test(self):
        from MetaDataApi.dataproviders.services import (
            DataProviderEtlService)

        from MetaDataApi.dataproviders.models import ThirdPartyDataProvider

        from MetaDataApi.metadata.models import Schema, Object

        data_provider = ThirdPartyDataProvider(
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
