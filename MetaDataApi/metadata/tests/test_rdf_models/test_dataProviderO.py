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
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import GrpDataProvider

        from MetaDataApi.metadata.tests import LoadTestData
        json_obj = LoadTestData.load_dummy_provider_json()

        dpo = GrpDataProvider(json_object=json_obj)
        self.assertEqual(2, len(dpo.endpoints))

        from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
        from MetaDataApi.metadata.models import ObjectInstance
        endpoints = list(ObjectInstance.objects.filter(base=RdfsDataProvider.SchemaItems.endpoint))
        self.assertEqual(2, len(endpoints))

        self.assertEqual(3, len(dpo.scope))

        endp_as_inst = list(map(lambda x: x.object_instance, dpo.endpoints))
        endp_as_inst.sort(key=lambda x: x.pk)
        endpoints.sort(key=lambda x: x.pk)
        self.assertListEqual(endp_as_inst, endpoints)
        self.assertEqual(dpo.api_type, "Oauth2-rest")

    def test_set_and_get_provider_atts(self):
        from MetaDataApi.metadata.rdfs_models.initialize_rdf_models import InitializeRdfModels
        InitializeRdfModels.create_all_schemas_from_descriptor()
        from MetaDataApi.metadata.rdfs_models.rdfs_data_provider.data_provider import GrpDataProvider
        dpo = GrpDataProvider()
        from MetaDataApi.metadata.tests import LoadTestData
        json_obj = LoadTestData.load_dummy_provider_json()
        del json_obj["client_id"], json_obj["client_secret"], json_obj["scope"], json_obj["endpoints"]
        for key, value in json_obj.items():
            setattr(dpo, key, value)
            returned_value = getattr(dpo, key)
            self.assertEqual(value, returned_value)

    def test_scopes_created_once_only(self):
        from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
        RdfsDataProvider.create_all_meta_objects()

        from MetaDataApi.metadata.tests import LoadTestData
        json_obj = LoadTestData.load_dummy_provider_json()

        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders
        InitializeDataProviders.create_if_does_not_exists(json_obj)
        dpo = InitializeDataProviders.create_if_does_not_exists(json_obj)
        self.assertEqual(3, len(dpo.scope))
