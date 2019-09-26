import django
from django.test import TransactionTestCase


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
            scope=["user.activity", "testscope"]
        )

    def test_build_auth_url(self):
        url = self.oauth.build_auth_url("99")
        expected = "https://account.withings.com/oauth2_user/authorize2" \
                   "?client_id=a80378abe1059ef7c415cf79b09b1270f828c4a0fbfdc52dbec06ae5f71b4bb6" \
                   "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2redirect&nounce=sdfkjlhasdfdhfas" \
                   "&response_type=code&response_mode=form_post&state=dummy%3A99&scope=user.activity+testscope"
        self.assertEqual(expected, url)

    def test_build_auth_url_without_scopes(self):
        self.oauth.scope = None
        self.oauth.save()
        url = self.oauth.build_auth_url("99")
        expected = "https://account.withings.com/oauth2_user/authorize2" \
                   "?client_id=a80378abe1059ef7c415cf79b09b1270f828c4a0fbfdc52dbec06ae5f71b4bb6" \
                   "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2redirect&nounce=sdfkjlhasdfdhfas" \
                   "&response_type=code&response_mode=form_post&state=dummy%3A99&scope=None"
        self.assertEqual(expected, url)
