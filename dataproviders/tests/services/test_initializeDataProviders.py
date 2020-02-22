from unittest.mock import patch

import django
from django.test import TransactionTestCase
from generic_serializer import SerializableModelFilter
from model_bakery import baker

from MetaDataApi.tests.utils_for_testing.utils_for_testing import get_method_path
from dataproviders.models import DataProvider, Endpoint
from dataproviders.models.RequestType import RequestType
from dataproviders.services.initialize_data_providers import InitializeDataProviders
from dataproviders.tests.mock_objects.mock_data_provider import MockDataProvider


class TestInitializeDataProviders(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestInitializeDataProviders, cls).setUpClass()
        django.setup()

    def test_load_one_provider(self):
        data = MockDataProvider.build_strava_data_provider_json()
        with patch(get_method_path(InitializeDataProviders.get_data_providers_from_local_or_remote_file)) as mock:
            mock.return_value = [data, ]
            InitializeDataProviders.load()
        data_provider = DataProvider.objects.get(provider_name="strava")
        self.assertEqual(data_provider.api_endpoint, data["api_endpoint"])

    def test_deserialize_serialize_provider(self):
        filter = SerializableModelFilter(
            exclude_labels=(),
            max_depth=2,
        )
        data_provider = baker.make(DataProvider, make_m2m=False)
        data = data_provider.serialize(filter=filter)
        new_dp = DataProvider.deserialize(data=data, filter=filter)
        self.assertEqual(new_dp.provider_name, data_provider.provider_name)

    def test_load_from_json(self):
        InitializeDataProviders.load()
        dps = DataProvider.objects.all()
        client_ids = list(map(lambda x: getattr(getattr(x, "oauth_config", None), "client_id", None), dps))
        expected_client_ids = ['a80378abe1059ef7c415cf79b09b1270f828c4a0fbfdc52dbec06ae5f71b4bb6', '28148',
                               'Q43N7PFF2RI3SF52',
                               '166351402500-m9302qf47ua66qbr1gdbgrronssnm2v2.apps.googleusercontent.com',
                               '166351402500-m9302qf47ua66qbr1gdbgrronssnm2v2.apps.googleusercontent.com',
                               '37b4731d-bb3a-4666-a4fa-6eb1fdffa146', 'acfb3400228146bdbd8dbf8de4046cd0', None, None,
                               None]
        self.assertListEqual(expected_client_ids, client_ids)

        ep = list(Endpoint.objects.all())

        endpoint_names = [x.endpoint_name for x in ep]

        expected_endpoint_names = ['sleep', 'athlete', 'activity', 'zone', 'athlete', 'user_info', 'sleep', 'activity',
                                   'readiness', 'data_source', 'notifications', 'recently_played', 'profile']

        self.assertListEqual(expected_endpoint_names, endpoint_names)

    def test_get_providers_from_aws(self):
        from dataproviders.services.initialize_data_providers import InitializeDataProviders

        json = InitializeDataProviders.get_providers_from_aws()
        assert len(json) > 10
        assert json[1]["provider_name"] == "endomondo"

    def test_create_strava_data_provider(self):
        from dataproviders.services.initialize_data_providers import InitializeDataProviders

        data = MockDataProvider.build_strava_data_provider_json()

        InitializeDataProviders.exclude = (
            "dataprovideruser",
            "data_provider_node",
            "data_fetches"
        )

        InitializeDataProviders.create_data_provider(data)

        strava_dp = DataProvider.objects.get(provider_name="strava")
        self.assertEqual(strava_dp.oauth_config.client_id, "28148")
        self.assertEqual(strava_dp.endpoints.get(endpoint_name="athlete").request_type, RequestType.GET.value)

    def test_update_data_provider_to_json_file(self):
        api_endpoint = "test_dummy_endpoint"
        dp = baker.make(DataProvider.__name__, make_m2m=True, provider_name="strava", api_endpoint=api_endpoint)

        def side_effect(data):
            data_provider = InitializeDataProviders.find_provider_with_name(data, dp)[1]
            self.assertEqual(data_provider["api_endpoint"], api_endpoint)
            return data

        with patch(get_method_path(InitializeDataProviders.write_data_to_json_file)) as mock_method:
            mock_method.side_effect = side_effect
            InitializeDataProviders.update_data_provider_to_json_file(dp)
        mock_method.assert_called_once()
