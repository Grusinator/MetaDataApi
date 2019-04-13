import io
from datetime import datetime

import django
from django.core.files import File
from django.test import TransactionTestCase


class TestRdfDataProvider(TransactionTestCase):
    provider_name = "dummyname"
    endpoint_name = "soome_endpoint"
    endpoint_url = "https://awesomeurl.it"

    @classmethod
    def setUpClass(cls):
        super(TestRdfDataProvider, cls).setUpClass()
        django.setup()

    def test_create_all_meta_objects(self):
        from MetaDataApi.metadata.rdf_models.meta_data_api.rdf_data_provider \
            import RdfDataProvider

        from MetaDataApi.metadata.tests.data import LoadTestData
        LoadTestData.init_foaf()
        items = RdfDataProvider.create_all_meta_objects()

        item_labels = [obj.label for obj in items]

        expected = ['data_provider', 'rest_endpoint', 'endpoint_data_dump', 'data_dump_file', 'date_downloaded',
                    'file_origin_url', 'endpoint_name', 'data_provider_name', 'has_generated', 'has_rest_endpoint',
                    'endpoint_template_url']

        item_labels.sort()
        expected.sort()
        self.assertEquals(expected, item_labels)

        assert RdfDataProvider.do_schema_items_exists()

    def test_create_data_provider(self):
        from MetaDataApi.metadata.rdf_models.meta_data_api.rdf_data_provider \
            import RdfDataProvider
        from MetaDataApi.metadata.models import ObjectInstance

        RdfDataProvider.create_all_meta_objects()
        provider = RdfDataProvider.create_data_provider(self.provider_name)
        instances = ObjectInstance.objects.all()

        self.assertTrue(provider in instances)

    def test_create_endpoint_to_data_provider(self):
        from MetaDataApi.metadata.rdf_models.meta_data_api.rdf_data_provider \
            import RdfDataProvider
        from MetaDataApi.metadata.models import ObjectInstance

        RdfDataProvider.create_all_meta_objects()

        provider = RdfDataProvider.create_data_provider(self.provider_name)
        endpoint = RdfDataProvider.create_endpoint_to_data_provider(
            provider,
            endpoint_name=self.endpoint_name,
            endpoint_url=self.endpoint_url
        )
        instances = ObjectInstance.objects.all()

        self.assertTrue(endpoint in instances)

    def test_create_data_dump(self):
        from MetaDataApi.metadata.rdf_models.meta_data_api.rdf_data_provider \
            import RdfDataProvider
        from MetaDataApi.metadata.models import ObjectInstance

        RdfDataProvider.create_all_meta_objects()

        provider = RdfDataProvider.create_data_provider(self.provider_name)
        endpoint = RdfDataProvider.create_endpoint_to_data_provider(
            provider,
            endpoint_name=self.endpoint_name,
            endpoint_url=self.endpoint_url
        )
        datadump = RdfDataProvider.create_data_dump(
            endpoint,
            datetime.now(),
            File(io.BytesIO(b"some initial text data"))
        )

        instances = ObjectInstance.objects.all()
        self.assertTrue(datadump in instances)

    def test_get_endpoint(self):
        from MetaDataApi.metadata.rdf_models.meta_data_api.rdf_data_provider \
            import RdfDataProvider

        RdfDataProvider.create_all_meta_objects()

        provider = RdfDataProvider.create_data_provider(self.provider_name)
        endpoint = RdfDataProvider.create_endpoint_to_data_provider(
            provider,
            endpoint_name=self.endpoint_name,
            endpoint_url=self.endpoint_url
        )

        fetched = RdfDataProvider.get_endpoint(provider, self.endpoint_name)

        self.assertEqual(endpoint, fetched)
