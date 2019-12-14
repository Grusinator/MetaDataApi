# import unittest
#
# import django
# from django.test import TransactionTestCase
#
#
# class TestDataProvider(TransactionTestCase):
#     """Tests for the application views."""
#
#     # Django requires an explicit setup() when running tests in PTVS
#     @classmethod
#     def setUpClass(cls):
#         super(TestDataProvider, cls).setUpClass()
#         django.setup()
#
#     def setUp(self):
#         from dataproviders.models.initialize_data_providers import InitializeDataProviders
#         InitializeDataProviders.load()
#
#     @unittest.skip("rdfs-related")
#     def test_create_data_provider_instance(self):
#         from dataproviders.models import DataProvider
#
#         data_provider = DataProvider(
#             provider_name="name",
#             api_endpoint="d",
#             authorize_url="d",
#             access_token_url="d",
#             client_id="d",
#             client_secret="d",
#             scope="d"
#         )
#         data_provider.save()
#
#         self.assertIsNotNone(data_provider.data_provider_node)
#         self.assertIsNotNone(data_provider.data_provider_node.pk)
#
#     @unittest.skip
#     def test_endpoints_are_created_at_provider_creation(self):
#         schema_label = "meta_data_api"
#
#         from MetaDataApi.utils.testing_utils import TestingUtils
#         meta_labels = set(TestingUtils.get_all_item_labels_from_schema(schema_label))
#
#         expected_labels = {
#             'meta_data_api', 'data_provider', 'endpoint_data_dump', 'api_type',
#             'data_provider_name', 'data_dump_file', 'date_downloaded', 'file_origin_url',
#             'endpoint_name', 'endpoint_url', 'has_generated', 'loaded',
#             'scope', 'provider_has_endpoint', 'endpoint', 'access_token_url',
#             'authorize_url', "api_endpoint"
#         }
#
#         self.assertSetEqual(meta_labels, expected_labels)
#
#     @unittest.skip
#     def test_urls_are_created_correct_reggression(self):
#         schema_label = "meta_data_api"
#
#         from metadata.utils.testing_utils import TestingUtils
#         instances = TestingUtils.get_all_object_instances_from_schema(schema_label)
#
#         endpoint_obj_inst = []
#
#         urls = []
#
#         expected_urls = [
#             'v2/sleep?action=getsummary&access_token={AuthToken:}&startdateymd={StartDateTime:Y-M-d}&enddateymd={EndDateTime:Y-M-d}',
#             'v2/sleep?action=get&access_token={AuthToken:}&startdate={StartDateTime:UTCSEC}&enddate={EndDateTime:UTCSEC}',
#             'v3/activities', 'v3/athlete/zones', 'v3/athlete', 'v1/userinfo',
#             'v1/sleep?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}',
#             'v1/activity?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}',
#             'v1/readiness?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}', 'v1/users/me/dataSources',
#             '/v3/notifications', 'v1/me/player/recently-played']
#         expected_urls.sort()
#         urls.sort()
#         self.assertListEqual(expected_urls, urls)
