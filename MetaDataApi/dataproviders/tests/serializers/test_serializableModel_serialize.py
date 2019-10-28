import django
from django.test import TransactionTestCase

from MetaDataApi.dataproviders.models.ApiTypes import ApiTypes


class TestSerializableModelSerialize(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSerializableModelSerialize, cls).setUpClass()
        django.setup()
        from MetaDataApi.dataproviders.models import DataProvider
        cls.model = DataProvider

    def test_serializing_provider_only(self):
        data_provider = self.model.objects.create(
            provider_name="dsfsd4"
        )
        from MetaDataApi.dataproviders.models.SerializableModelFilter import SerializableModelFilter
        data = data_provider.serialize(filter=SerializableModelFilter(max_depth=0))
        expected = {'provider_name': 'dsfsd4', 'api_type': 'OauthRest', 'api_endpoint': ''}
        self.assertDictEqual(expected, data)

    def test_serializing_provider_and_oauth(self):
        from MetaDataApi.dataproviders.models import OauthConfig

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
        from MetaDataApi.dataproviders.models.SerializableModelFilter import SerializableModelFilter
        data = data_provider.serialize(
            filter=SerializableModelFilter(max_depth=1, exclude_labels=("dataproviderprofile",)))

        expected = {
            'provider_name': 'dsfsd6', 'api_type': 'OauthRest', 'api_endpoint': '', 'endpoints': [],
            'http_config': None,
            'oauth_config': {
                'authorize_url': 'test',
                'access_token_url': 'test.dk',
                'client_id': '123',
                'client_secret': 'test',
                'scope': ['234'],
            },
            'data_provider_node': None
        }
        self.assertEqual(expected, data)

    def test_serializing_provider_and_endpoints(self):
        data_provider = self.create_data_provider_with_endpoints()

        from MetaDataApi.dataproviders.models.SerializableModelFilter import SerializableModelFilter
        data = data_provider.serialize(
            filter=SerializableModelFilter(max_depth=1, exclude_labels=("dataproviderprofile",)))
        expected = {'provider_name': 'dsfsd4', 'api_type': 'OauthGraphql', 'api_endpoint': '',
                    'endpoints': [
                        {'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET'},
                        {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET'}
                    ],
                    'http_config': None, 'oauth_config': None, 'data_provider_node': None}
        self.assertEqual(expected, data)

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
