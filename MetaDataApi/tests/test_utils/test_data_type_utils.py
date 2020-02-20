from datetime import datetime

import django
from django.test import TransactionTestCase
from json2model.services import data_type_transform


class TestJsonUtils(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestJsonUtils, cls).setUpClass()
        django.setup()

    def test_identify_data_type(self):
        input_vs_expected = [
            ("20.40", float),
            (2.4, float),
            ("2012-01-19 17:21:00", datetime),
            ('2018-10-02T16: 16: 49Z', datetime),
            # ("2019-20-04:20:30:59", datetime),
            (2, int),
            ("1", int),
            ("test", str),
            ("False", bool),
            (True, bool),
            (None, type(None))
        ]

        inputd, expected = zip(*input_vs_expected)

        resp = [type(data_type_transform.transform_data_type(elm)) for elm in inputd]

        self.assertListEqual(list(resp), list(expected))
