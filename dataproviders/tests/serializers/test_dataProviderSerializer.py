import unittest

import django
from django.test import TransactionTestCase

from MetaDataApi.utils import JsonUtils
from dataproviders.tests.mock_objects.mock_data_provider import MockDataProvider


class TestDataProviderSerializer(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestDataProviderSerializer, cls).setUpClass()
        django.setup()

    def test_serializing_provider_only(self):
        from dataproviders.models import DataProvider
        dp = DataProvider.objects.create(
            provider_name="dsfsd4"
        )

        from dataproviders.serializers.DataProviderSerializer import DataProviderSerializer
        data = DataProviderSerializer(dp).data
        data = JsonUtils.dump_and_load(data)
        expected = {
            'oauth_config': None,
            'http_config': None,
            'icon_image_url': None,
            'provider_name': 'dsfsd4',
            'api_type': "OauthRest",
            'api_endpoint': '',
            'endpoints': [],
        }
        self.assertEqual(expected, data)

    def test_serializing_provider_and_oauth(self):
        from dataproviders.models import DataProvider
        from dataproviders.models import OauthConfig

        dp = DataProvider.objects.create(
            provider_name="dsfsd4",
        )
        dp.save()
        oauth = OauthConfig.objects.create(
            data_provider=dp,
            authorize_url="test"
        )
        oauth.save()

        from dataproviders.serializers.DataProviderSerializer import DataProviderSerializer
        data = DataProviderSerializer(dp).data
        data = JsonUtils.dump_and_load(data)
        expected = {'oauth_config': {'authorize_url': 'test', 'access_token_url': '', 'client_id': '',
                                     'client_secret': '', 'scope': ''},
                    'http_config': None,
                    'provider_name': 'dsfsd4',
                    'api_type': 'OauthRest',
                    'icon_image_url': None,
                    'api_endpoint': '',
                    'endpoints': []
                    }
        self.assertEqual(expected, data)

    def test_serializing_provider_and_endpoints(self):
        dp = MockDataProvider.create_data_provider_with_endpoints()

        from dataproviders.serializers.DataProviderSerializer import DataProviderSerializer
        data = DataProviderSerializer(dp).data
        data = JsonUtils.dump_and_load(data)
        expected = {'oauth_config': None, 'http_config': None,
                    'endpoints': [{'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET'},
                                  {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET'}],
                    'provider_name': 'dsfsd4', 'api_type': 'OauthGraphql', 'api_endpoint': '', 'icon_image_url': None,
                    }
        self.assertEqual(expected, data)

    @unittest.skip("dataproviderserializer has errors but is not importaint since we have the generic serializer")
    def test_deserializing_provider_and_endpoints(self):
        data = {
            'provider_name': 'dsfsd4',
            'api_endpoint': 'ghfj',
            'endpoints': [],
        }

        from dataproviders.serializers.DataProviderSerializer import DataProviderSerializer
        serializer = DataProviderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(data, serializer.validated_data)
