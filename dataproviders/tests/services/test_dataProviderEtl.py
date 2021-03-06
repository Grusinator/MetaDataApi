# import unittest
#
# import django
# from django.test import TransactionTestCase
# from MetaDataApi.utils import JsonUtils
#
# from dataproviders.models.ApiTypes import ApiTypes
#
#
# class TestDataProviderEtlService(TransactionTestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         super(TestDataProviderEtlService, cls).setUpClass()
#         django.setup()
#         from dataproviders.models.initialize_data_providers import InitializeDataProviders
#         InitializeDataProviders.load()
#
#     @unittest.skip("needs cleanup this is not what this test is supposed to do")
#     def test_headers_are_built_correctly(self):
#         from dataproviders.models import DataProvider
#         data_provider = DataProvider.objects.get(provider_name="tinder")
#
#         #from metadata.tests import LoadTestData
#         user = LoadTestData.init_user()
#         profile = LoadTestData.init_profile(user)
#         from dataproviders.models import DataProviderUser
#         dp_profile = DataProviderUser.objects.create(
#             profile=profile,
#             data_provider=data_provider,
#             access_token="12345"
#         )
#
#         self.assertEqual(data_provider.api_type, ApiTypes.TOKEN_REST.value)
#
#     @unittest.skip(
#         "this integration test needs to be run against a static env. how? or at least not test on return data")
#     def test_read_data_from_endpoint_correctly(self):
#         from metadata.tests import LoadTestData
#
#         from dataproviders.models.initialize_data_providers import InitializeDataProviders
#         InitializeDataProviders.load()
#         dp_profile = LoadTestData.init_strava_data_provider_profile()
#         LoadTestData.create_dummy_provider(dp_profile)
#
#         from dataproviders.services import FetchDataFromProvider
#         service = FetchDataFromProvider(dp_profile.data_provider)
#
#         endpoint_name = "activity"
#
#         data = service._fetch_data_from_endpoint(endpoint_name, dp_profile.access_token)
#
#         json_data = JsonUtils.validate(data)
#
#         expected = [{'resource_state': 2, 'athlete': {'id': 41124303, 'resource_state': 1}, 'name': 'Morning Run',
#                      'distance': 3218.7, 'moving_time': 3600, 'elapsed_time': 3600, 'total_elevation_gain': 3.0,
#                      'type': 'Run', 'workout_type': 2, 'id': 2291228399, 'external_id': None, 'upload_id': None,
#                      'start_date': '2019-04-15T17:10:00Z', 'start_date_local': '2019-04-15T10:10:00Z',
#                      'timezone': '(GMT-08:00) America/Los_Angeles', 'utc_offset': -25200.0, 'start_latlng': None,
#                      'end_latlng': None, 'location_city': None, 'location_state': None, 'location_country': None,
#                      'start_latitude': None, 'start_longitude': None, 'achievement_count': 0, 'kudos_count': 0,
#                      'comment_count': 0, 'athlete_count': 1, 'photo_count': 0,
#                      'map': {'id': 'a2291228399', 'summary_polyline': None, 'resource_state': 2}, 'trainer': False,
#                      'commute': True, 'manual': True, 'private': False, 'visibility': 'everyone', 'flagged': False,
#                      'gear_id': None, 'from_accepted_tag': None, 'average_speed': 0.894, 'max_speed': 0.0,
#                      'has_heartrate': False, 'heartrate_opt_out': False, 'display_hide_heartrate_option': False,
#                      'pr_count': 0, 'total_photo_count': 0, 'has_kudoed': False}]
#
#         self.assertEqual(expected, json_data)
