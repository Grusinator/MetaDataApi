from datetime import datetime
from unittest import TestCase

from MetaDataApi.dataproviders.services.url_format_helper import UrlFormatHelper


class TestUrlFormatHelper(TestCase):
    def test_build_args_for_url(self):
        start_time = datetime(2018, 3, 4)
        end_time = datetime(2018, 5, 4)

        endpoint = "testendpoint?start={StartDateTime:UTCSEC}&end={EndDateTime:UTCSEC}"

        output_endpoint = UrlFormatHelper.build_args_for_url(
            endpoint, StartDateTime=start_time, EndDateTime=end_time)

        expected = "testendpoint?start=1520118000&end=1525384800"

        self.assertEqual(expected, output_endpoint)
