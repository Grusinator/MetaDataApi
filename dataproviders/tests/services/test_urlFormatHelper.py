from datetime import datetime, timedelta
from unittest import TestCase

from dataproviders.models import Endpoint, UrlArg
from dataproviders.models.UrlArgFormatter import UrlArgFormatter
from dataproviders.models.UrlArgType import UrlArgType
from dataproviders.services.url_args_formatter.args_rule_types import *
from dataproviders.services.url_args_formatter.url_formatter import UrlFormatter


class TestUrlFormatHelper(TestCase):
    def test_build_args_for_url(self):
        start_time = datetime(2018, 3, 4)
        end_time = datetime(2018, 5, 4)
        access_token = "dummy"
        selected = [
            StartDateTime(datetime.now() - timedelta(days=30)),
            EndDateTime(datetime.now()),
            AuthToken(access_token),
            PageCurrent(0),
            PageSize(100)
        ]

        endpoint = Endpoint.objects.create(endpoint_url="testendpoint")
        UrlArg.objects.create(key_name="start", arg_type=UrlArgType.START_DATE_TIME,
                              value_formatter=UrlArgFormatter.TIME_Y_M_D, endpoint=endpoint)
        UrlArg.objects.create(key_name="end", arg_type=UrlArgType.END_DATE_TIME,
                              value_formatter=UrlArgFormatter.TIME_Y_M_D, endpoint=endpoint)
        UrlArg.objects.create(key_name="token", arg_type=UrlArgType.AUTH_TOKEN, endpoint=endpoint)

        output_endpoint = UrlFormatter.build_args_for_url(endpoint, selected)
        expected = f"testendpoint?start={start_time.timestamp()}&end={end_time.timestamp()}"
        self.assertEqual(expected, output_endpoint)
