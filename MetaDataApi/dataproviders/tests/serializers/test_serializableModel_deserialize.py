import logging

import django

from MetaDataApi.dataproviders.tests.mock_data.MockDataProvider import MockDataProvider

logging.basicConfig(level=logging.DEBUG)

from django.test import TransactionTestCase


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
        data = MockDataProvider.build_base_with_endpoints_data()

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
                    "data_dumps",
                ),
                start_object_name="data_provider"
            )
        )

        self.assertEqual(dp.provider_name, data["provider_name"])
        self.assertEqual(dp.endpoints.count(), 2)
        self.assertEqual(dp.api_type, data["api_type"])
        self.assertEqual(dp.endpoints.first().endpoint_url, data["endpoints"][0]["endpoint_url"])

    def test_deserializing_configs_both(self):
        data = MockDataProvider.build_full_data()

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
        data = MockDataProvider.build_base_with_http_data()

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
        data = MockDataProvider.build_base_with_http_data()

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

