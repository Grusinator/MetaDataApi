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

    def test_deserializing_provider_and_endpoints(self):
        data = {
            'provider_name': 'dsfsd4',
            'api_type': ApiTypes.OAUTH_GRAPHQL.name,
            'api_endpoint': '56',
            'endpoints': [
                {'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET'},
                {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET'}
            ],
            # 'http_config': None,
            # 'oauth_config': None,
            # 'data_provider_node': None
        }

        from MetaDataApi.dataproviders.models import DataProvider
        data_out = DataProvider.deserialize(
            data, max_depth=1,
            exclude=(
                "dataproviderprofile",
                "oauth_config",
                "http_config",
                "data_provider_node",
            )
        )

        self.assertEqual(data, data_out)

    def test_deserializing_configs(self):
        # AssertionError: The `.create()` method does not support writable nested fields by default.
        # Write an explicit `.create()` method for serializer `rest_framework.serializers.DataProviderSerializer`,
        # or set `read_only=True` on nested serializer fields.

        data = self.build_data()

        from MetaDataApi.dataproviders.models import DataProvider
        data_out = DataProvider.deserialize(
            data, max_depth=1,
            exclude=(
                "dataproviderprofile",
                # "oauth_config",
                # "http_config",
                "data_provider_node",
                # "data_provider",
                # "endpoints",
                "scope",
                "header",
                "url_encoded_params"
            )
        )

        dp = DataProvider(**data)
        self.maxDiff = None
        self.assertDictEqual(data, data_out)

    def build_data(self):
        data = {
            'provider_name': 'dsfsd4', 'api_type': ApiTypes.OAUTH_GRAPHQL.name, 'api_endpoint': '56',
            'endpoints': [
                {'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET'},
                {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET'}
            ],
            "oauth_config": {
                "authorize_url": "https://account.withings.com/oauth2_user/authorize2",
                "access_token_url": "https://account.withings.com/oauth2/token",
                "client_id": "123",
                "client_secret": "12345",
                "scope": ["user.activity"]
            },
            "http_config": {
                "header": {
                    "User-Agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
                    "X-Auth-Token": "{AuthToken:}",
                    "Content-Type": "application/json"
                },
                "url_encoded_params": {
                    "d": "a",
                    "c": "t"
                },
            }
        }
        return data
