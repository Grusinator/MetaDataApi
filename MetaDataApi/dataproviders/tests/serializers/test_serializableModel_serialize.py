import django
from django.test import TransactionTestCase

from MetaDataApi.dataproviders.tests.mock_data.MockDataProvider import MockDataProvider


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
        data_provider = MockDataProvider.create_data_provider_with_endpoints()

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

    def test_serialization_of_strava(self):
        dp = MockDataProvider.build_strava_data_provider_objects()

    def test_deserialization_of_strava(self):
        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders

        data = MockDataProvider.build_strava_data_provider_json()

        InitializeDataProviders.exclude = (
            "dataproviderprofile",
            "data_provider_node",
        )

        InitializeDataProviders.create_data_provider_v2(data)

        from MetaDataApi.dataproviders.models import DataProvider
        strava_dp = DataProvider.objects.get(provider_name="strava")
        self.assertEqual(strava_dp.oauth_config.client_id, "28148")
        self.assertEqual(strava_dp.endpoints.get(endpoint_name="athlete").data_dumps.first().date_downloaded,
                         "20102019")
