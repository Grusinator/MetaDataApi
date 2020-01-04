import unittest

import django
from django.test import TransactionTestCase

from dataproviders.tests.mock_objects.mock_data_provider import MockDataProvider


class TestSerializableModelSerialize(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSerializableModelSerialize, cls).setUpClass()
        django.setup()
        from dataproviders.models import DataProvider
        cls.model = DataProvider
        cls.exclude_labels = (
            "dataprovideruser",
        )
        cls.data_provider_name = "data_provider"

    def test_serializing_provider_only(self):
        data_provider = self.model.objects.create(
            provider_name="dsfsd4"
        )
        from generic_serializer import SerializableModelFilter
        data = data_provider.serialize(filter=SerializableModelFilter(max_depth=0))
        expected = {'provider_name': 'dsfsd4', 'api_type': 'OauthRest', 'api_endpoint': ''}
        self.assertDictEqual(expected, data)

    @unittest.skip("move to Serializer project, failing due to known issues")
    def test_serializing_provider_and_oauth(self):
        from dataproviders.models import OauthConfig

        data_provider = self.model.objects.create(
            provider_name="dsfsd6",
        )
        data_provider.save()
        oauth = OauthConfig.objects.create(
            data_provider=data_provider,
            authorize_url="test",
            access_token_url="test.dk",
            client_id="123",
            client_secret="test",
            scope=['234', ]

        )
        oauth.save()
        from generic_serializer import SerializableModelFilter
        data = data_provider.serialize(
            filter=SerializableModelFilter(max_depth=1,
                                           exclude_labels=self.exclude_labels + ("endpoints", "http_config")))

        expected = {
            'provider_name': 'dsfsd6',
            'api_type': 'OauthRest',
            'api_endpoint': '',
            'endpoints': [],
            'oauth_config': {
                'authorize_url': 'test',
                'access_token_url': 'test.dk',
                'client_id': '123',
                'client_secret': 'test',
                'scope': ['234'],
            },

        }
        self.assertDictEqual(expected, data)

    @unittest.skip("move to Serializer project, failing due to known issues")
    def test_serializing_provider_and_endpoints(self):
        data_provider = MockDataProvider.create_data_provider_with_endpoints()

        from generic_serializer import SerializableModelFilter
        data = data_provider.serialize(
            filter=SerializableModelFilter(max_depth=1, exclude_labels=("dataprovideruser",),
                                           start_object_name="data_provider"))
        expected = {
            'provider_name': 'dsfsd4',
            'api_type': 'OauthGraphql',
            'api_endpoint': '',
            'endpoints': [
                {'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET'},
                {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET'}
            ]
        }
        self.assertEqual(expected, data)

    @unittest.skip("fails because validated data on data dumps are not correct, needs fixing.")
    def test_serialization_of_strava(self):
        dp = MockDataProvider.build_strava_data_provider_objects()
