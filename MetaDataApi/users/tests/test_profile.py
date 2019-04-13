import django
from django.test import TransactionTestCase


class TestProfile(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestProfile, cls).setUpClass()
        django.setup()

    def test_create_profile(self):
        from MetaDataApi.users.models import Profile
        from MetaDataApi.users.models import Languages

        from MetaDataApi.metadata.tests import LoadTestData
        LoadTestData.init_foaf()
        user = LoadTestData.init_user()
        profile = Profile(
            language=Languages.Danish,
            user=user
        )
        profile.save()

        self.assertIsNotNone(profile.foaf_person)
