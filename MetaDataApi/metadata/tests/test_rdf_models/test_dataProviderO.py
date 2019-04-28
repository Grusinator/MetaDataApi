import django
from django.test import TransactionTestCase


class TestDataProviderO(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestDataProviderO, cls).setUpClass()
        django.setup()

    def test_create_provider(self):
        from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
        RdfsDataProvider.create_all_meta_objects()

        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import DataProviderO

        dpo = DataProviderO(
            json_object={
                "provider_name": "strava",
                "api_type": "Oauth2-rest",
                "api_endpoint": "https://www.strava.com/api/",
                "authorize_url": "https://www.strava.com/oauth/authorize",
                "access_token_url": "https://www.strava.com/oauth/token",
                "client_id": "12345",
                "client_secret": "very_secret",
                "scope": ["scope1", "scope2", "scope3"],
                "rest_endpoints_list": [
                    {
                        "name": "activity",
                        "url": "v3/activities"
                    },
                    {
                        "name": "zone",
                        "url": "v3/athlete/zones"
                    },
                ],
                "json_schema_file_url": "dummy"
            }
        )

        from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
        from MetaDataApi.metadata.models import ObjectInstance
        endpoints = list(ObjectInstance.objects.filter(base=RdfsDataProvider.SchemaItems.endpoint))
        self.assertEqual(2, len(endpoints))

        self.assertEqual(3, len(dpo.scope))

        endp_as_inst = list(map(lambda x: x.self_ref, dpo.endpoints))
        self.assertListEqual(endp_as_inst, endpoints)
