import django
from django.test import TransactionTestCase

from MetaDataApi.dataproviders.models.third_party_data_provider import ApiTypes


class TestDataProvider(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDataProvider, cls).setUpClass()
        django.setup()

    def test_create_profile(self):
        from MetaDataApi.dataproviders.models import ThirdPartyDataProvider

        from MetaDataApi.metadata.models import Schema
        schema = Schema(label="meta_data_api", url="test.com")
        schema.save()

        from MetaDataApi.metadata.models import Object
        object = Object(label="data_provider", schema=schema)
        object.save()

        data_provider = ThirdPartyDataProvider(
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
