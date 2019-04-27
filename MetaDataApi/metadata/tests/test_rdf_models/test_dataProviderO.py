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
        from MetaDataApi.dataproviders.models import DataProvider
        dataprovider = DataProvider(
            provider_name="template",
            api_endpoint="endp",
            authorize_url="auth",
            access_token_url="",
            scope=["scope1", "scope2", "scope3"],
            rest_endpoints_list=[
                {"name": "user_info", "url": "v1/userinfo"},
                {"name": "sleep", "url": "v1/sleep"},
                {"name": "activity", "url": "v1/activity"},
                {"name": "readiness", "url": "v1/readiness"}
            ],
            json_schema_file_url="schema_url"
        )

        dpo = DataProviderO(
            db_data_provider=dataprovider
        )

        from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
        from MetaDataApi.metadata.models import ObjectInstance
        endpoints = list(ObjectInstance.objects.filter(base=RdfsDataProvider.SchemaItems.endpoint))
        self.assertEqual(4, len(endpoints))
