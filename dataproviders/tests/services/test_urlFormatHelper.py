from datetime import datetime
from unittest import TestCase

from dataproviders.services.url_format_helper import UrlFormatHelper


class TestUrlFormatHelper(TestCase):
    def test_build_args_for_url(self):
        start_time = datetime(2018, 3, 4)
        end_time = datetime(2018, 5, 4)

        endpoint = "testendpoint?start={StartDateTime:UTCSEC}&end={EndDateTime:UTCSEC}"

        output_endpoint = UrlFormatHelper.build_args_for_url(
            endpoint, StartDateTime=start_time, EndDateTime=end_time)

        expected = "testendpoint?start=%i&end=%i" % (start_time.timestamp(), end_time.timestamp())

        self.assertEqual(expected, output_endpoint)
