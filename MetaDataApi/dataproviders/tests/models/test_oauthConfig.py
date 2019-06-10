import django
from django.test import TransactionTestCase

from MetaDataApi.metadata.utils import JsonUtils


class TestOauthConfig(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestOauthConfig, cls).setUpClass()
        django.setup()

    def setUp(self) -> None:
        from MetaDataApi.dataproviders.models import OauthConfig, DataProvider
        self.data_provider = DataProvider.objects.create(provider_name="dummy")
        self.oauth = OauthConfig.objects.create(
            data_provider=self.data_provider,
            authorize_url="https://account.withings.com/oauth2_user/authorize2",
            access_token_url="https://account.withings.com/oauth2/token",
            client_id="a80378abe1059ef7c415cf79b09b1270f828c4a0fbfdc52dbec06ae5f71b4bb6",
            client_secret="122345",
            scope=JsonUtils.dumps([
                "user.activity", "testscope"
            ])
        )

    def test_build_auth_url(self):
        url = self.oauth.build_auth_url("99")
        expected = ""
        self.assertEqual(expected, url)

    def test_build_auth_url_without_scopes(self):
        del self.oauth.scope
        url = self.oauth.build_auth_url("99")
        expected = ""
        self.assertEqual(expected, url)
