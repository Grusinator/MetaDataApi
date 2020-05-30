import django
from django.test import TransactionTestCase

from MetaDataApi.utils import JsonUtils
from dataproviders.serializers import DataProviderSerializer
from dataproviders.tests.mock_objects.mock_data_provider import MockDataProvider


class TestDataProviderSerializer(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()

    def test_serialize(self):
        dp = MockDataProvider.create_data_provider_with_endpoints()
        serializer = DataProviderSerializer(dp)
        expected = {'oauth_config': None, 'http_config': None, 'endpoints': [
            {'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET', 'api_type': 'OauthGraphql'},
            {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET', 'api_type': 'OauthGraphql'}],
                    'icon_image_url': None, 'provider_name': 'test_provider_name', 'provider_url': None,
                    'api_endpoint': "test_endpoint"}
        data = JsonUtils.validate(serializer.data)
        self.assertEqual(data, expected)

    def test_deserialize(self):
        data = MockDataProvider.build_full_data()
        serializer = DataProviderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        expected = {
            'oauth_config': {
                'scope': ['user.activity'],
                'authorize_url': 'https://account.withings.com/oauth2_user/authorize2',
                'access_token_url': 'https://account.withings.com/oauth2/token',
                'client_id': '123', 'client_secret': '12345'},
            'http_config': {
                'url_encoded_params': {'d': 'a', 'c': 't'},
                'header': {'User-Agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)',
                           'X-Auth-Token': '{AuthToken:}', 'Content-Type': 'application/json'}},
            'endpoints': [
                {'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET',
                 'api_type': 'rest'},
                {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET',
                 'api_type': 'rest'}
            ],
            'icon_image_url': 'http://someurl.com/image',
            'provider_name': 'test_provider_name', 'provider_url': None, 'api_endpoint': '56'}
        serializer.save()
        serialized_data = JsonUtils.validate(serializer.data)
        self.assertDictEqual(serialized_data, expected)
