import django
from django.test import TransactionTestCase

from MetaDataApi.dataproviders.models.ApiTypes import ApiTypes


class TestSerializableModelSerializer(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSerializableModelSerializer, cls).setUpClass()
        django.setup()
        from MetaDataApi.dataproviders.models import DataProvider
        cls.model = DataProvider

    def test_serializing_provider_only(self):
        data_provider = self.model.objects.create(
            provider_name="dsfsd4"
        )

        data = data_provider.serialize(depth=0)
        expected = {
            'oauth_config': None,
            'http_config': None,
            'provider_name': 'dsfsd423',
            'api_type': "OauthRest",
            'api_endpoint': '',
            'data_provider_node': None
        }
        self.assertEqual(expected, data)

    def test_serializing_provider_and_oauth(self):
        from MetaDataApi.dataproviders.models import OauthConfig

        data_provider = self.model.objects.create(
            provider_name="dsfsd4",
        )
        data_provider.save()
        oauth = OauthConfig.objects.create(
            data_provider=data_provider,
            authorize_url="test"
        )
        oauth.save()
        data = data_provider.serialize()

        expected = {'oauth_config': {'authorize_url': 'test', 'access_token_url': '', 'client_id': '',
                                     'client_secret': '', 'scope': ''},
                    'http_config': None,
                    'provider_name': 'dsfsd4',
                    'api_type': 'OauthRest',
                    'api_endpoint': '',
                    'data_provider_node': None}
        self.assertEqual(expected, data)

    def test_serializing_provider_and_endpoints(self):
        data_provider = self.create_data_provider_with_endpoints()

        data = data_provider.serialize()
        expected = {'oauth_config': None, 'http_config': None,
                    'endpoints': [{'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET'},
                                  {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET'}],
                    'provider_name': 'dsfsd4', 'api_type': 'OauthGraphql', 'api_endpoint': '',
                    'data_provider_node': None}
        self.assertEqual(expected, data)

    def test_deserializing_provider_and_endpoints(self):
        data = {
            'provider_name': 'dsfsd4',
            'api_endpoint': 'ghfj'
        }

        from MetaDataApi.dataproviders.serializers.DataProviderSerializer import DataProviderSerializer
        serializer = DataProviderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(data, serializer.validated_data)

    def create_data_provider_with_endpoints(self):
        data_provider = self.model.objects.create(
            provider_name="dsfsd4",
            api_type=ApiTypes.OAUTH_GRAPHQL.value
        )
        data_provider.save()
        from MetaDataApi.dataproviders.models import Endpoint
        endpoint = Endpoint.objects.create(
            data_provider=data_provider,
            endpoint_name="test1",
            endpoint_url="testurl"
        )
        endpoint.save()
        endpoint2 = Endpoint.objects.create(
            data_provider=data_provider,
            endpoint_name="test2",
            endpoint_url="testurl"
        )
        endpoint2.save()
        return data_provider
