import django
from django.test import TransactionTestCase

from MetaDataApi.metadata.utils.django_model_utils import DjangoModelUtils


class TestRdfsDataProvider(TransactionTestCase):
    provider_name = "dummyname"
    endpoint_name = "soome_endpoint"
    endpoint_url = "https://awesomeurl.it"

    @classmethod
    def setUpClass(cls):
        super(TestRdfsDataProvider, cls).setUpClass()
        django.setup()

    def test_create_all_meta_objects(self):
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider \
            import RdfsDataProvider

        from MetaDataApi.metadata.tests.data import LoadTestData
        LoadTestData.init_foaf()
        items = RdfsDataProvider.create_all_meta_objects()

        item_labels = [obj.label for obj in items]

        expected = [
            'api_type', 'data_dump_file', 'data_provider', 'data_provider_name', 'date_downloaded', 'endpoint',
            'endpoint_data_dump', 'endpoint_name', 'endpoint_url', 'file_origin_url', 'has_generated',
            'loaded', 'provider_has_endpoint', 'scope'
        ]

        item_labels.sort()
        expected.sort()
        self.assertEquals(expected, item_labels)

        assert RdfsDataProvider.do_schema_items_exists()

    def test_create_data_provider(self):
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider \
            import RdfsDataProvider
        from MetaDataApi.metadata.models import ObjectInstance

        RdfsDataProvider.create_all_meta_objects()
        provider = RdfsDataProvider.create_data_provider(self.provider_name)
        instances = ObjectInstance.objects.all()

        self.assertTrue(provider in instances)

    def test_create_endpoint_to_data_provider(self):
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider \
            import RdfsDataProvider
        from MetaDataApi.metadata.models import ObjectInstance

        RdfsDataProvider.create_all_meta_objects()

        provider = RdfsDataProvider.create_data_provider(self.provider_name)
        endpoint = RdfsDataProvider.create_endpoint_to_data_provider(
            provider,
            endpoint_name=self.endpoint_name,
            endpoint_url=self.endpoint_url
        )
        instances = ObjectInstance.objects.all()

        self.assertTrue(endpoint in instances)

    def test_create_data_dump(self):
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider \
            import RdfsDataProvider
        from MetaDataApi.metadata.models import ObjectInstance

        RdfsDataProvider.create_all_meta_objects()

        provider = RdfsDataProvider.create_data_provider(self.provider_name)
        endpoint = RdfsDataProvider.create_endpoint_to_data_provider(
            provider,
            endpoint_name=self.endpoint_name,
            endpoint_url=self.endpoint_url
        )
        datadump = RdfsDataProvider.create_data_dump(
            endpoint,
            DjangoModelUtils.convert_str_to_file("dummy text")
        )

        instances = ObjectInstance.objects.all()
        self.assertTrue(datadump in instances)

    def test_get_endpoint(self):
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider \
            import RdfsDataProvider

        RdfsDataProvider.create_all_meta_objects()

        provider = RdfsDataProvider.create_data_provider(self.provider_name)
        endpoint = RdfsDataProvider.create_endpoint_to_data_provider(
            provider,
            endpoint_name=self.endpoint_name,
            endpoint_url=self.endpoint_url
        )

        fetched = RdfsDataProvider.get_endpoint(provider, self.endpoint_name)

        self.assertEqual(endpoint, fetched)
