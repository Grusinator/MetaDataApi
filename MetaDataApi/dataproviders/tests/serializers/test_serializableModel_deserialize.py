import logging

import django

logging.basicConfig(level=logging.DEBUG)

from django.test import TransactionTestCase

from MetaDataApi.dataproviders.models.ApiTypes import ApiTypes


class TestSerializableModelSerialize(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSerializableModelSerialize, cls).setUpClass()
        django.setup()
        from MetaDataApi.dataproviders.models import DataProvider
        cls.model = DataProvider
        cls.exclude_labels = (
            "dataproviderprofile",
            # "oauth_config",
            # "http_config",
            "data_provider_node",
            # "data_provider",
            # "endpoints",
            # "scope",
            # "header",
            # "url_encoded_params",
            "data_dumps"
        )

    def test_deserializing_provider_and_endpoints(self):
        data = self.build_base_with_endpoints_data()

        from MetaDataApi.dataproviders.models import DataProvider
        from MetaDataApi.dataproviders.models.SerializableModelFilter import SerializableModelFilter
        dp = DataProvider.deserialize(
            data,
            filter=SerializableModelFilter(
                max_depth=3,
                exclude_labels=(
                    "dataproviderprofile",
                    "oauth_config",
                    "http_config",
                    "data_provider_node",
                    "data_dumps"
                ),
                start_object_name="data_provider"
            )
        )

        self.assertEqual(dp.provider_name, data["provider_name"])
        self.assertEqual(dp.endpoints.count(), 2)
        self.assertEqual(dp.api_type, data["api_type"])
        self.assertEqual(dp.endpoints.first().endpoint_url, data["endpoints"][0]["endpoint_url"])

    def test_deserializing_configs_both(self):
        data = self.build_full_data()

        from MetaDataApi.dataproviders.models import DataProvider
        from MetaDataApi.dataproviders.models.SerializableModelFilter import SerializableModelFilter
        dp = DataProvider.deserialize(
            data,
            filter=SerializableModelFilter(
                max_depth=3,
                exclude_labels=self.exclude_labels,
                start_object_name="data_provider"
            )
        )

        self.assertEqual(dp.oauth_config.client_id, data["oauth_config"]["client_id"])
        self.assertEqual(dp.oauth_config.authorize_url, data["oauth_config"]["authorize_url"])

        self.assertEqual(dp.oauth_config.scope, data["oauth_config"]["scope"])

        self.assertEqual(dp.http_config.url_encoded_params, data["http_config"]["url_encoded_params"])
        self.assertEqual(dp.http_config.header, data["http_config"]["header"])

    def test_deserializing_configs_http(self):
        data = self.build_base_with_http_data()

        from MetaDataApi.dataproviders.models import DataProvider
        from MetaDataApi.dataproviders.models.SerializableModelFilter import SerializableModelFilter
        dp = DataProvider.deserialize(
            data,
            filter=SerializableModelFilter(
                max_depth=3,
                exclude_labels=self.exclude_labels,
                start_object_name="data_provider"
            )
        )

        self.assertFalse(hasattr(dp, "oauth_config"))
        self.assertEqual(dp.http_config.url_encoded_params, data["http_config"]["url_encoded_params"])
        self.assertEqual(dp.http_config.header, data["http_config"]["header"])

    def test_deserializing_configs_oauth(self):
        data = self.build_base_with_http_data()

        from MetaDataApi.dataproviders.models import DataProvider
        from MetaDataApi.dataproviders.models.SerializableModelFilter import SerializableModelFilter
        dp = DataProvider.deserialize(
            data,
            filter=SerializableModelFilter(
                max_depth=3,
                exclude_labels=self.exclude_labels,
                start_object_name="data_provider"
            )
        )

        self.assertFalse(hasattr(dp, "http_config"))
        self.assertEqual(dp.oauth_config.client_id, data["oauth_config"]["client_id"])
        self.assertEqual(dp.oauth_config.authorize_url, data["oauth_config"]["authorize_url"])

    def build_full_data(self):
        return {
            **self.build_base_data(),
            **self.build_http_data(),
            **self.build_oauth_data(),
            # **self.build_endpoints_data()
        }

    def build_base_with_http_data(self):
        return {**self.build_base_data(), **self.build_http_data()}

    def build_base_with_oauth_data(self):
        return {**self.build_base_data(), **self.build_oauth_data()}

    def build_base_with_endpoints_data(self):
        return {**self.build_base_data(), **self.build_endpoints_data()}

    def build_base_data(self):
        return {
            'provider_name': 'dsfsd4', 'api_type': ApiTypes.OAUTH_GRAPHQL.value, 'api_endpoint': '56',
            'endpoints': [
                {'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET'},
                {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET'}
            ]
        }

    def build_oauth_data(self):
        return {
            "oauth_config": {
                "authorize_url": "https://account.withings.com/oauth2_user/authorize2",
                "access_token_url": "https://account.withings.com/oauth2/token",
                "client_id": "123",
                "client_secret": "12345",
                "scope": ["user.activity"]
            }
        }

    def build_http_data(self):
        return {
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

    def build_endpoints_data(self):
        return {
            'endpoints': [
                {'endpoint_name': 'test1', 'endpoint_url': 'testurl', 'request_type': 'GET'},
                {'endpoint_name': 'test2', 'endpoint_url': 'testurl', 'request_type': 'GET'}
            ]
        }
