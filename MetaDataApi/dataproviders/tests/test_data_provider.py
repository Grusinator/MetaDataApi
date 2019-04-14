import django
from django.test import TransactionTestCase

from MetaDataApi.dataproviders.models.data_provider import ApiTypes
from MetaDataApi.metadata.models import ObjectInstance


class TestDataProvider(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDataProvider, cls).setUpClass()
        django.setup()
        from MetaDataApi.metadata.rdf_models import RdfDataProvider
        RdfDataProvider.create_all_meta_objects()
        from MetaDataApi.dataproviders.models.load_default_data_providers import LoadDefaultDataProviders
        LoadDefaultDataProviders.load()

    def test_create_profile(self):
        from MetaDataApi.dataproviders.models import DataProvider

        from MetaDataApi.metadata.models import Schema
        schema = Schema(label="meta_data_api", url="test.com")
        schema.save()

        from MetaDataApi.metadata.models import Object
        object = Object(label="data_provider", schema=schema)
        object.save()

        data_provider = DataProvider(
            provider_name="name",
            api_type=ApiTypes.OauthRest,
            api_endpoint="d",
            authorize_url="d",
            access_token_url="d",
            client_id="d",
            client_secret="d",
            scope="d",
            rest_endpoints_list="d",
        )
        data_provider.save()

        self.assertIsNotNone(data_provider.data_provider_instance)

    def test_endpoints_are_created_at_provider_creation(self):
        from MetaDataApi.dataproviders.models.load_default_data_providers import LoadDefaultDataProviders
        LoadDefaultDataProviders.load()

        from MetaDataApi.metadata.rdf_models import RdfDataProvider
        schema_label = RdfDataProvider.SchemaItems.schema.label

        from MetaDataApi.metadata.utils.testing_utils import TestingUtils
        meta_labels = TestingUtils.get_all_item_labels_from_schema(schema_label)

        expected_labels = ['meta_data_api', 'data_provider', 'endpoint_data_dump', 'rest_endpoint',
                           'data_provider_name', 'data_dump_file', 'date_downloaded', 'file_origin_url',
                           'endpoint_name', 'endpoint_template_url', 'has_generated', 'has_rest_endpoint']

        self.assertListEqual(meta_labels, expected_labels)

        instances = TestingUtils.get_all_object_instances_from_schema(schema_label)

        endpoint_obj_inst = list(filter(
            lambda x: isinstance(x, ObjectInstance) and
                      x.base.label == RdfDataProvider.SchemaItems.rest_endpoint.label,
            instances
        ))

        urls = list(map(lambda x:
                        x.get_att_inst(
                            RdfDataProvider.SchemaItems.endpoint_template_url.label).value,
                        endpoint_obj_inst))

        expected_urls = [
            'v2/sleep?action=getsummary&access_token={AuthToken:}&startdateymd={StartDateTime:Y-M-d}&enddateymd={EndDateTime:Y-M-d}',
            'v2/sleep?action=get&access_token={AuthToken:}&startdate={StartDateTime:UTCSEC}&enddate={EndDateTime:UTCSEC}',
            '/v3/activities', '/v3/athlete/zones', '/v3/athlete', '/v1/userinfo',
            '/v1/sleep?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}',
            '/v1/activity?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}',
            '/v1/readiness?start={StartDateTime:Y-M-d}&end={EndDateTime:Y-M-d}', 'v1/users/me/dataSources'
        ]

        self.assertListEqual(urls, expected_urls)
