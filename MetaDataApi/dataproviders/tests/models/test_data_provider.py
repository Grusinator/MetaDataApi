import json

import django
from django.test import TransactionTestCase


class TestDataProvider(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDataProvider, cls).setUpClass()
        django.setup()

    def setUp(self):
        from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
        RdfsDataProvider.create_all_meta_objects()
        from MetaDataApi.dataproviders.models.initialize_data_providers import InitializeDataProviders
        InitializeDataProviders.load()

    def test_create_data_provider_instance(self):
        from MetaDataApi.dataproviders.models import DataProvider
        from MetaDataApi.dataproviders.models.data_provider import ApiTypes

        data_provider = DataProvider(
            provider_name="name",
            api_type=ApiTypes.OauthRest,
            api_endpoint="d",
            authorize_url="d",
            access_token_url="d",
            client_id="d",
            client_secret="d",
            scope="d",
            rest_endpoints_list=json.dumps([{"name": "dummy", "url": "test.com"}])
        )
        data_provider.save()

        self.assertIsNotNone(data_provider.data_provider_instance)
        self.assertIsNotNone(data_provider.data_provider_instance.pk)

    def test_endpoints_are_created_at_provider_creation(self):
        from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
        schema_label = RdfsDataProvider.SchemaItems.schema.label

        from MetaDataApi.metadata.utils.testing_utils import TestingUtils
        meta_labels = set(TestingUtils.get_all_item_labels_from_schema(schema_label))

        expected_labels = {'meta_data_api', 'data_provider', 'endpoint_data_dump', 'rest_endpoint',
                           'data_provider_name', 'data_dump_file', 'date_downloaded', 'file_origin_url',
                           'endpoint_name', 'endpoint_template_url', 'has_generated', 'has_rest_endpoint', 'loaded'}

        self.assertSetEqual(meta_labels, expected_labels)

    def test_urls_are_created_correct_reggression(self):
        from MetaDataApi.metadata.rdfs_models import RdfsDataProvider
        schema_label = RdfsDataProvider.SchemaItems.schema.label

        from MetaDataApi.metadata.utils.testing_utils import TestingUtils
        instances = TestingUtils.get_all_object_instances_from_schema(schema_label)

        from MetaDataApi.metadata.models import ObjectInstance
        endpoint_obj_inst = list(filter(
            lambda x: isinstance(x, ObjectInstance) and
                      x.base.label == RdfsDataProvider.SchemaItems.endpoint.label,
            instances
        ))

        urls = list(map(lambda x:
                        x.get_att_inst_with_label(
                            RdfsDataProvider.SchemaItems.endpoint_template_url.label).value,
                        endpoint_obj_inst))

        expected_urls = [
            'v2/sleep?action=getsummary&access_token={AuthToken:}&startdateymd={StartDateTime:Y-M-d}&enddateymd={EndDateTime:Y-M-d}',
            'v2/sleep?action=get&access_token={AuthToken:}&startdate={StartDateTime:UTCSEC}&enddate={EndDateTime:UTCSEC}',
            'v3/activities', 'v3/athlete/zones', 'v3/athlete', 'v1/userinfo',
            'v1/sleep?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}',
            'v1/activity?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}',
            'v1/readiness?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}', 'v1/users/me/dataSources',
            '/v3/notifications', 'v1/me/player/recently-played']

        self.assertListEqual(urls, expected_urls)
