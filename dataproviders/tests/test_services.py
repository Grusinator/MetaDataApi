# import unittest
#
# import django
# from django.test import TransactionTestCase
# from metadata.services.services import GetTemporalFloatPairsService
# from metadata.tests.data import LoadTestData
#
#
# class TestSomeService(TransactionTestCase):
#
#     # Django requires an explicit setup() when running tests in PTVS
#     @classmethod
#     def setUpClass(cls):
#         super(TestSomeService, cls).setUpClass()
#         django.setup()
#
#     @unittest.skip("needs repair")
#     def test_some(self):
#         LoadTestData.init_strava_schema_from_file()
#         LoadTestData.init_strava_data_from_file()
#
#         args = {
#             "schema_label": "strava",
#             "object_label": "activities",
#             "attribute_label": "distance",
#             "datetime_label": "name",
#             "datetime_object_label": "activities",
#         }
#
#         data = GetTemporalFloatPairsService.execute(args)
#
#         expected = []
#
#         self.assertListEqual(data, expected)
