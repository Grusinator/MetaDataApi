import django
from django.test import TransactionTestCase

from metadata.services.services import GetTemporalFloatPairsService
from metadata.tests.data import LoadTestData


class TestService(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestService, cls).setUpClass()
        django.setup()

    def test_get_temporal_attribute(self):

        LoadTestData.init_strava_schema_from_file()
        LoadTestData.init_strava_data_from_file()

        args = {
            "schema_label": "strava",
            "object_label": "activities",
            "attribute_label": "distance",
            "datetime_label": "start_date",
            "datetime_object_label": "activities",
        }

        data = GetTemporalFloatPairsService.execute(args)

        expected = [(3503.7, '2018-10-02 16:16:49+00:00'),
                    (3133.3, '2018-09-30 06:29:17+00:00'),
                    (3555.6, '2018-09-28 08:59:08+00:00'),
                    (3926.8, '2018-09-26 05:45:27+00:00'),
                    (4774.5, '2018-09-24 07:45:02+00:00'),
                    (4395.6, '2018-09-20 06:30:42+00:00'),
                    (11867.8, '2018-09-12 15:09:44+00:00')]

        # extract the values instead of objects
        data_values = [(att_inst1.value, str(att_inst2.value))
                       for att_inst1, att_inst2 in data]

        self.assertListEqual(data_values, expected)
