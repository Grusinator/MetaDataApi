import django
from django.test import TransactionTestCase


class TestInitializeDataProviders(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestInitializeDataProviders, cls).setUpClass()
        django.setup()

    def test_load_from_json(self):
        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders
        InitializeDataProviders.load()

        from MetaDataApi.dataproviders.models import DataProvider
        dps = DataProvider.objects.all()

        from MetaDataApi.dataproviders.models import Endpoint

        client_ids = list(map(lambda x: x.oauth_config.client_id, dps))

        expected_client_ids = ['', 'a80378abe1059ef7c415cf79b09b1270f828c4a0fbfdc52dbec06ae5f71b4bb6', '28148',
                               'Q43N7PFF2RI3SF52',
                               '166351402500-m9302qf47ua66qbr1gdbgrronssnm2v2.apps.googleusercontent.com',
                               '166351402500-m9302qf47ua66qbr1gdbgrronssnm2v2.apps.googleusercontent.com', '',
                               '37b4731d-bb3a-4666-a4fa-6eb1fdffa146', '284033629198396',
                               'acfb3400228146bdbd8dbf8de4046cd0', '']

        self.assertListEqual(expected_client_ids, client_ids)

        ep = list(Endpoint.objects.all())

        endpoint_names = list(map(lambda x: x.endpoint_name, ep))

        expected_endpoint_names = ['sleep', 'athlete', 'activity', 'zone', 'athlete', 'user_info', 'sleep', 'activity',
                                   'readiness', 'data_source', 'notifications', 'recently_played']

        self.assertListEqual(expected_endpoint_names, endpoint_names)

    def test_get_providers_from_aws(self):
        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders

        json = InitializeDataProviders.get_providers_from_aws()
        assert len(json) > 10
        assert json[0]["provider_name"] == "endomondo"

    def test_deserialization_of_strava(self):
        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders

        data = self.build_strava_data_provider_json()

        InitializeDataProviders.exclude = (
            "dataproviderprofile",
            "data_provider_node",
            "data_dump",
            "data_dumps",
            "http_config"
        )

        InitializeDataProviders.create_data_provider_v2(data)

        from MetaDataApi.dataproviders.models import DataProvider
        strava = DataProvider.objects.get(provider_name="strava")
        self.assertEqual(strava.oauth_config.client_id, "28148")

    def build_strava_data_provider_json(self):
        return {
            "provider_name": "strava",
            "api_type": "OauthRest",
            "api_endpoint": "https://www.strava.com/api/",
            "oauth_config": {
                "authorize_url": "https://www.strava.com/oauth/authorize",
                "access_token_url": "https://www.strava.com/oauth/token",
                "client_id": "28148",
                "client_secret": "ed5f469f798830c7214fc8efad54790799fc3ae1",
                "scope": [
                    "view_private"
                ]
            },
            "endpoints": [
                {
                    "endpoint_name": "activity",
                    "endpoint_url": "v3/activities"
                },
                {
                    "endpoint_name": "zone",
                    "endpoint_url": "v3/athlete/zones"
                },
                {
                    "endpoint_name": "athlete",
                    "endpoint_url": "v3/athlete"
                }
            ]
        }
